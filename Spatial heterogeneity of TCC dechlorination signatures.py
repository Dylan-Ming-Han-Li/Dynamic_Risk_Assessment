# -*- coding: utf-8 -*-

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from shapely.geometry import box
from matplotlib.colors import BoundaryNorm, ListedColormap
import matplotlib.patches as patches


# ===============================
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 7,
    'axes.labelsize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'axes.linewidth': 0.4,
    'xtick.major.width': 0.4,
    'ytick.major.width': 0.4,
    'svg.fonttype': 'path',     
    'savefig.transparent': True
})
sns.set_style("white")

TARGET_CRS = "EPSG:4326"
MAIN_XLIM = (73, 135)
MAIN_YLIM = (18, 54)


# ===============================
china_provinces = gpd.read_file('省级.shp')
china_borders   = gpd.read_file('国家矢量.shp')
nine_dash_line  = gpd.read_file('九段线.shp')

data = pd.read_excel('140个点数据.xlsx').astype({
    'Longitude': 'float',
    'Latitude': 'float',
    'TCC': 'float',
    'Risk': 'float',
    'DCC_TCC': 'float'
})
data.rename(columns={'DCC_TCC': 'DCC/TCC'}, inplace=True)


# ===============================
def ensure_crs(gdf, target_crs=TARGET_CRS):
    if gdf.crs is None:
        gdf = gdf.set_crs(target_crs)
    else:
        gdf = gdf.to_crs(target_crs)
    return gdf

china_provinces = ensure_crs(china_provinces)
china_borders   = ensure_crs(china_borders)
nine_dash_line  = ensure_crs(nine_dash_line)


# ===============================
gdf = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(data.Longitude, data.Latitude),
    crs=TARGET_CRS
)

np.random.seed(42)
jitter = 0.5  

gdf['lon_j'] = gdf['Longitude'] + np.random.uniform(-jitter, jitter, len(gdf))
gdf['lat_j'] = gdf['Latitude']  + np.random.uniform(-jitter, jitter, len(gdf))

gdf_j = gpd.GeoDataFrame(
    gdf.drop(columns='geometry'),
    geometry=gpd.points_from_xy(gdf['lon_j'], gdf['lat_j']),
    crs=TARGET_CRS
)

# ===============================
# 分类与配色
# ===============================
bounds = [0.102, 0.34, 1, 14.726]
colors = ['#f7fbff', '#77A3BA', '#B92A4A']
cmap   = ListedColormap(colors)
norm   = BoundaryNorm(bounds, cmap.N)

# ===============================
main_bbox = gpd.GeoDataFrame(
    geometry=[box(MAIN_XLIM[0], MAIN_YLIM[0], MAIN_XLIM[1], MAIN_YLIM[1])],
    crs=TARGET_CRS
)

prov_main = gpd.clip(china_provinces, main_bbox)
bord_main = gpd.clip(china_borders, main_bbox)
gdf_main  = gpd.clip(gdf_j, main_bbox)


# ===============================
size_factor = 3
legend_labels = [2, 5, 10, 20]

fig, ax = plt.subplots(figsize=(4, 3.2), facecolor='none')
fig.patch.set_alpha(0)
ax.set_facecolor('none')
ax.set_position([0.07, 0.16, 0.78, 0.74])

prov_main.plot(
    ax=ax,
    color='none',
    edgecolor='0.9',
    linewidth=0.4,
    zorder=1
)

bord_main.plot(
    ax=ax,
    color='none',
    edgecolor='0.8',
    linewidth=0.4,
    zorder=2
)

sc = ax.scatter(
    gdf_main.geometry.x,
    gdf_main.geometry.y,
    s=gdf_main['Risk'] * size_factor,
    c=gdf_main['DCC/TCC'],
    cmap=cmap,
    norm=norm,
    alpha=0.6,
    edgecolor='black',
    linewidth=0.2,
    zorder=3
)


# ===============================
mean_val = gdf_main['DCC/TCC'].mean()
cax = fig.add_axes([0.1, 0.18, 0.28, 0.028])
cax.set_facecolor('none')

cbar = fig.colorbar(sc, cax=cax, orientation='horizontal')
cbar.ax.tick_params(labelsize=7, width=0.4, length=0.5)
cbar.ax.set_title('Dechlorination Activity (DCC/TCC)', fontsize=7, fontname='Arial')

cbar.set_ticks([min(bounds), mean_val, max(bounds)])
cbar.set_ticklabels([
    f'{min(bounds):.1f}',
    f'mean: {mean_val:.1f}    ',
    f'{max(bounds):.1f}'
])

cbar.ax.tick_params(which='both', length=0)
cbar.ax.tick_params(which='major', length=2)


# ===============================
ax.set_xlim(*MAIN_XLIM)
ax.set_ylim(*MAIN_YLIM)
ax.set_aspect(1 / np.cos(np.deg2rad(35)))  

ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_visible(True)

ax.spines['top'].set_linewidth(0.4)
ax.spines['left'].set_linewidth(0.4)

ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')
ax.set_xticks([80, 100, 120])
ax.set_xticklabels(['80°E', '100°E', '120°E'])

ax.yaxis.set_ticks_position('left')
ax.set_yticks([20, 30, 40, 50])
ax.set_yticklabels(['20°N', '30°N', '40°N', '50°N'])

ax.tick_params(
    axis='both',
    direction='out',
    length=2,
    width=0.4,
    color='black',
    labelsize=7
)


# ===============================
xmin, ymin, xmax, ymax = nine_dash_line.total_bounds
pad_x = (xmax - xmin) * 0.12
pad_y = (ymax - ymin) * 0.12

inset_ax = fig.add_axes([0.82, 0.16, 0.11, 0.20], facecolor='none')

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

inset_ax.set_xlim(xmin - pad_x, xmax + pad_x)
inset_ax.set_ylim(ymin - pad_y, ymax + pad_y)
inset_ax.set_xticks([])
inset_ax.set_yticks([])
inset_ax.set_facecolor('none')

for spine in inset_ax.spines.values():
    spine.set_linewidth(0.4)

# ===============================
# Risk 图例
# ===============================
lg_ax = fig.add_axes([0.16, 0.46, 0.12, 0.18])
lg_ax.set_facecolor('none')

label_width = 2

for lab in legend_labels:
    lg_ax.scatter(
        [], [],
        s=lab * size_factor,
        color='none',
        alpha=0.8,
        edgecolor='k',
        linewidth=0.4,
        label=f'{lab:^{label_width}}'
    )

lg = lg_ax.legend(
    title='Integrated risk',
    title_fontsize=7,
    frameon=False,
    loc='upper left',
    handletextpad=0.8,
    labelspacing=0.9,
    handlelength=0.8
)

lg.get_title().set_fontweight('normal')

for t in lg.get_texts():
    t.set_fontfamily('DejaVu Sans Mono')
    t.set_ha('center')

lg_ax.axis('off')

# ===============================
# 三个虚线框（经纬度下直接画，和当前显示方式一致）
# ===============================
boxes = [
    (115, 37.5, 4, 4, "Beijing-Tianjin-Heibei", (124, 36.5)),
    (116.5, 29.2, 7, 5, "Yangtze River Delta", (124.5, 31)),
    (110.5, 20, 4, 4, "Greater Bay Area", (114.8, 19.4))
]

for x, y, w, h, label, pos in boxes:
    rect = patches.Rectangle(
        (x, y),
        w, h,
        linewidth=0.6,
        edgecolor='#EAAA60',
        linestyle='--',
        facecolor='none',
        zorder=4
    )
    ax.add_patch(rect)

    ax.text(
        pos[0], pos[1],
        label,
        fontsize=7,
        color='#EAAA60',
        ha='left',
        fontstyle='italic',
        zorder=5
    )


# ===============================
plt.subplots_adjust(left=0.03, right=0.97, top=0.96, bottom=0.08)


# ===============================
plt.savefig(
    '活性分布NG.svg',
    format='svg',
    bbox_inches='tight',
    pad_inches=0.04,
    transparent=True,
    facecolor='none',
    edgecolor='none'
)

plt.show()