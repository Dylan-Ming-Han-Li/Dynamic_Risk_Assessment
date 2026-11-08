import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from shapely.geometry import box
from matplotlib.patches import Patch, Wedge, Circle
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, DrawingArea

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 8

# 统一各类文字元素字号
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['legend.title_fontsize'] = 8


mpl.rcParams['svg.fonttype'] = 'path'


mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42


mpl.rcParams['mathtext.fontset'] = 'dejavusans'
mpl.rcParams['mathtext.default'] = 'regular'
mpl.rcParams['axes.unicode_minus'] = False

# Parameters
# =========================
TARGET_CRS = "EPSG:4326"

MAIN_XLIM = (73, 135)
MAIN_YLIM = (18, 54)

COLOR_TCC = '#B92A4A'
COLOR_TCS = '#77A3BA'
PROV_FILL = '#f7f7f7'
PROV_EDGE = '0.6'

SIZE_MIN_VAL = 3
SIZE_MAX_VAL = 20
SIZE_MIN_PT = 4      
SIZE_MAX_PT = 10      
RING_FRAC = 0.3       

OUTPUT_NAME = 'HAMs_distribution_map'

# =========================
# Helper functions
# =========================
def ensure_crs(gdf, target_crs=TARGET_CRS):
    """Make sure layer has a CRS and transform to target CRS."""
    if gdf.crs is None:
        gdf = gdf.set_crs(target_crs)
    else:
        gdf = gdf.to_crs(target_crs)
    return gdf


def size_to_diameter_pts(
    val,
    vmin=SIZE_MIN_VAL,
    vmax=SIZE_MAX_VAL,
    dmin=SIZE_MIN_PT,
    dmax=SIZE_MAX_PT
):
    """Map concentration to donut diameter in points using sqrt scaling."""
    if pd.isna(val) or val <= 0:
        return 0

    val = np.clip(val, vmin, vmax)

    t = (
        (np.sqrt(val) - np.sqrt(vmin))
        / (np.sqrt(vmax) - np.sqrt(vmin))
    )

    return dmin + t * (dmax - dmin)


def add_donut(
    ax,
    x,
    y,
    tcc,
    tcs,
    total_val,
    colors=(COLOR_TCC, COLOR_TCS),
    ring_frac=RING_FRAC
):
    """
    Draw a donut chart centered at (x, y) in data coordinates.

    The central area of the donut is transparent.
    """
    if pd.isna(tcc) or pd.isna(tcs):
        return

    if (tcc + tcs) <= 0:
        return

    diameter = size_to_diameter_pts(total_val)

    if diameter <= 0:
        return


    da = DrawingArea(
        diameter,
        diameter,
        0,
        0,
        clip=False
    )

    radius = diameter / 2
    center = (radius, radius)

    values = [tcc, tcs]
    total = sum(values)

    start_angle = 90

    for value, color in zip(values, colors):
        angle = 360 * value / total

        da.add_artist(
            Wedge(
                center=center,
                r=radius,
                theta1=start_angle,
                theta2=start_angle + angle,
                width=radius * ring_frac,
                facecolor=color,
                edgecolor='none',
                linewidth=0
            )
        )

        start_angle += angle

    da.add_artist(
        Circle(
            center,
            radius=radius,
            facecolor='none',
            edgecolor='none',
            linewidth=0
        )
    )

    annotation = AnnotationBbox(
        da,
        (x, y),
        xycoords='data',
        frameon=False,
        box_alignment=(0.5, 0.5),
        pad=0
    )

    ax.add_artist(annotation)



# Read spatial files
# =========================
china_provinces = ensure_crs(
    gpd.read_file('省级.shp')
)

china_borders = ensure_crs(
    gpd.read_file('国家矢量.shp')
)

nine_dash_line = ensure_crs(
    gpd.read_file('九段线.shp')
)

# =========================
# Read data
# =========================
data = pd.read_excel(
    '1.污染-脱氯-风险数据.xlsx'
)

data.columns = data.columns.str.strip()

cols = [
    'Longitude',
    'Latitude',
    'TCC_TOC',
    'TCS_TOC',
    'HAMs_TOC'
]

data[cols] = data[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

data = data.dropna(
    subset=['Longitude', 'Latitude']
)

data[
    ['TCC_TOC', 'TCS_TOC', 'HAMs_TOC']
] = data[
    ['TCC_TOC', 'TCS_TOC', 'HAMs_TOC']
].fillna(0)

gdf = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(
        data['Longitude'],
        data['Latitude']
    ),
    crs=TARGET_CRS
)


# Main map clipping
# =========================
main_bbox = gpd.GeoDataFrame(
    geometry=[
        box(
            MAIN_XLIM[0],
            MAIN_YLIM[0],
            MAIN_XLIM[1],
            MAIN_YLIM[1]
        )
    ],
    crs=TARGET_CRS
)

prov_main = gpd.clip(
    china_provinces,
    main_bbox
)

bord_main = gpd.clip(
    china_borders,
    main_bbox
)

gdf_main = gpd.clip(
    gdf,
    main_bbox
)


# Figure
# =========================
fig, ax = plt.subplots(
    figsize=(4.6, 3.8),
    facecolor='none'
)

ax.set_position([
    0.06,
    0.13,
    0.80,
    0.78
])

ax.set_facecolor('none')


prov_main.plot(
    ax=ax,
    color=PROV_FILL,
    edgecolor='0.9',
    linewidth=0.4,
    zorder=1
)


bord_main.plot(
    ax=ax,
    color='none',
    edgecolor='0.7',
    linewidth=0.4,
    zorder=2
)


for _, row in gdf_main.iterrows():
    add_donut(
        ax=ax,
        x=row.geometry.x,
        y=row.geometry.y,
        tcc=row['TCC_TOC'],
        tcs=row['TCS_TOC'],
        total_val=row['HAMs_TOC']
    )


# Main map axes
# =========================
ax.set_xlim(*MAIN_XLIM)
ax.set_ylim(*MAIN_YLIM)

ax.set_aspect(
    1 / np.cos(np.deg2rad(35))
)

ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_visible(True)

ax.spines['top'].set_linewidth(0.4)
ax.spines['left'].set_linewidth(0.4)

ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

ax.set_xticks([
    80,
    100,
    120
])

ax.set_xticklabels([
    '80°E',
    '100°E',
    '120°E'
])

ax.yaxis.set_ticks_position('left')

ax.set_yticks([
    20,
    30,
    40,
    50
])

ax.set_yticklabels([
    '20°N',
    '30°N',
    '40°N',
    '50°N'
])

ax.tick_params(
    axis='both',
    direction='out',
    length=2,
    width=0.4,
    color='black',
    labelsize=8
)

# =========================
# South China Sea inset
# =========================
xmin, ymin, xmax, ymax = nine_dash_line.total_bounds

pad_x = (xmax - xmin) * 0.12
pad_y = (ymax - ymin) * 0.12

inset_ax = fig.add_axes(
    [0.74, 0.23, 0.14, 0.15],
    facecolor='none'
)

china_provinces.plot(
    ax=inset_ax,
    color='none',
    edgecolor='lightgrey',
    linewidth=0.4
)

nine_dash_line.plot(
    ax=inset_ax,
    color='lightgrey',
    linewidth=0.4
)

inset_ax.set_xlim(
    xmin - pad_x,
    xmax + pad_x
)

inset_ax.set_ylim(
    ymin - pad_y,
    ymax + pad_y
)

inset_ax.set_xticks([])
inset_ax.set_yticks([])
inset_ax.set_facecolor('none')

for spine in inset_ax.spines.values():
    spine.set_linewidth(0.4)

# =========================
# Composition legend
# =========================
legend_elements = [
    Patch(
        facecolor=COLOR_TCC,
        edgecolor='none',
        label='TCC'
    ),
    Patch(
        facecolor=COLOR_TCS,
        edgecolor='none',
        label='TCS'
    )
]

leg1 = ax.legend(
    handles=legend_elements,
    loc='lower left',
    bbox_to_anchor=(0.01, 0.9),
    frameon=False,
    ncol=2,
    fontsize=8,
    handlelength=1.5,
    columnspacing=1,
    handletextpad=0.6
)

ax.add_artist(leg1)

# =========================
# Size legend
# =========================
legend_vals = [
    2,
    5,
    10,
    20
]

size_handles = [
    Line2D(
        [0],
        [0],
        marker='o',
        linestyle='None',
        markerfacecolor='none',
        markeredgecolor='0.4',
        markeredgewidth=0.6,
        markersize=size_to_diameter_pts(v),
        label=f'{v}'
    )
    for v in legend_vals
]

leg2 = ax.legend(
    handles=size_handles,
    title='ΣHAMs (μg g$^{-1}$ TOC)',
    title_fontsize=8,
    fontsize=8,
    frameon=False,
    loc='lower left',
    bbox_to_anchor=(0.1, 0.315),
    labelspacing=0.8,
    borderpad=0.2,
    handletextpad=0.8
)

# =========================
# Transparent background
# =========================
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
inset_ax.patch.set_alpha(0)

# =========================
# Save
# =========================
# 先完成画布渲染，再保存
fig.canvas.draw()

fig.savefig(
    f'{OUTPUT_NAME}.svg',
    dpi=1200,
    format='svg',
    bbox_inches='tight',
    pad_inches=0.01,
    transparent=True,
    facecolor='none',
    edgecolor='none'
)

fig.savefig(
    f'{OUTPUT_NAME}.pdf',
    format='pdf',
    bbox_inches='tight',
    pad_inches=0.01,
    transparent=True,
    facecolor='none',
    edgecolor='none'
)

# =========================
# Preview
# =========================
plt.show()