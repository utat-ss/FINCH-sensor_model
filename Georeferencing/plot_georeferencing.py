import rasterio
import matplotlib.pyplot as plt
import numpy as np


TIFF_PATH = "output/salt_flat_with_gcps.tiff"

GCP_ROWS = np.array([295, 362, 160, 625, 146, 262])
GCP_COLS = np.array([207, 142, 316, 234, 130, 268])

TEST_ROWS = np.array([40, 508, 458])
TEST_COLS = np.array([150, 200, 391])

GCP_COLOR = "black"
TEST_COLOR = "#13562B"


def plot_points(ax, x, y, labels, color, marker="o", show_coords=False):
    """Plot and annotate GCPs or test points."""
    ax.scatter(
        x,
        y,
        color=color,
        s=90,
        marker=marker,
        edgecolor="white" if marker == "o" else "black",
        linewidth=1.5,
        label=labels,
        zorder=5,
    )

    for i, (px, py) in enumerate(zip(x, y), start=1):
        label = f"{labels.rstrip('s')} {i}"

        if show_coords:
            label += f"\n({px:.4f}, {py:.4f})"

        ax.annotate(
            label,
            (px, py),
            xytext=(8, 8),
            textcoords="offset points",
            color=color,
            fontsize=9,
            zorder=6,
        )


def main():
    # Load raster data and georeferencing information.
    with rasterio.open(TIFF_PATH) as src:
        image = src.read()
        transform = src.transform
        bounds = src.bounds
        crs = src.crs

    # Convert raster bands to a format suitable for Matplotlib.
    if image.shape[0] == 1:
        display_image = image[0]
    else:
        display_image = np.moveaxis(image[:3], 0, -1)

    # Convert pixel coordinates to map coordinates.
    gcp_x, gcp_y = transform * (GCP_COLS, GCP_ROWS)
    test_x, test_y = transform * (TEST_COLS, TEST_ROWS)

    # Create side-by-side plots.
    fig, (ax_pixel, ax_geo) = plt.subplots(
        1, 2, figsize=(16, 8)
    )

    # --------------------------------------------------
    # LEFT: Pixel coordinates
    # --------------------------------------------------

    ax_pixel.imshow(display_image, origin="upper")
    ax_pixel.set(
        title="Pixel Coordinates",
        xlabel="Column (x)",
        ylabel="Row (y)",
    )
    ax_pixel.grid(True, color="white", alpha=0.3)

    plot_points(
        ax_pixel,
        GCP_COLS,
        GCP_ROWS,
        "GCPs",
        GCP_COLOR,
    )

    plot_points(
        ax_pixel,
        TEST_COLS,
        TEST_ROWS,
        "Test Points",
        TEST_COLOR,
        marker="^",
    )

    ax_pixel.legend()

    # --------------------------------------------------
    # RIGHT: Geographic coordinates
    # --------------------------------------------------

    ax_geo.imshow(
        display_image,
        extent=[
            bounds.left,
            bounds.right,
            bounds.bottom,
            bounds.top,
        ],
        origin="upper",
        aspect="auto",
    )

    ax_geo.set(
        title="Geographic Coordinates",
        xlabel="Longitude",
        ylabel="Latitude",
    )
    ax_geo.grid(True, color="white", alpha=0.3)

    plot_points(
        ax_geo,
        gcp_x,
        gcp_y,
        "GCPs",
        GCP_COLOR,
        show_coords=True,
    )

    plot_points(
        ax_geo,
        test_x,
        test_y,
        "Test Points",
        TEST_COLOR,
        marker="^",
        show_coords=True,
    )

    ax_geo.legend()

    # --------------------------------------------------
    # Interactive coordinate display
    # --------------------------------------------------

    def on_mouse_move(event):
        if (
            event.inaxes is ax_pixel
            and event.xdata is not None
            and event.ydata is not None
        ):
            x, y = transform * (event.xdata, event.ydata)

            fig.suptitle(
                f"Pixel: column={event.xdata:.1f}, "
                f"row={event.ydata:.1f}  →  "
                f"X={x:.6f}, Y={y:.6f}",
                fontsize=12,
            )
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect(
        "motion_notify_event",
        on_mouse_move,
    )

    if crs is not None:
        fig.suptitle(f"Georeferencing Visualization ({crs})")

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()