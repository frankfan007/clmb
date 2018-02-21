"""Helper functions for MHT plots."""

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import matplotlib.colors
from numpy.random import RandomState
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
import numpy as np
import cf


CMAP = matplotlib.colors.ListedColormap(RandomState(0).rand(256*256, 3))


def eigsorted(cov):
    """Return eigenvalues, sorted."""
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:, order]


def cov_ellipse(cov, nstd):
    """Get the covariance ellipse."""
    vals, vecs = eigsorted(cov)
    r1, r2 = nstd * np.sqrt(vals)
    theta = np.arctan2(*vecs[:, 0][::-1])

    return r1, r2, theta


def plot_history(history, origin, c=0, covellipse=True, min_r=0, max_back=None, r_values=False, track_id=False, velocity=False, trace=True, **kwargs):
    """Plot single trace."""
    max_back = max_back or 0
    lines = {}
    for t, summaries in history[-max_back:]:
        for s in summaries:
            if s.id not in lines:
                lines[s.id] = [[], [], [], []]
            lines[s.id][0].append(s.r)
            lines[s.id][1].append(np.concatenate((cf.ll2ne(s.x[0:2], origin), s.x[2:])))
            lines[s.id][2].append(s.P)
            lines[s.id][3].append(s.cid)
    for s in summaries:
        if s.r < min_r:
            del lines[s.id]
    for id_, (rs, xs, Ps, cids) in lines.items():
        cl = c + id_
        if trace:
            plt.plot([x[0] for x in xs], [x[1] for x in xs], color=CMAP(cl), **kwargs)
            for cid, x in zip(cids, xs):
                plt.plot(x[0], x[1], 's', fillstyle='none', color=CMAP(cid), **kwargs)

        if covellipse:
            ca = plot_cov_ellipse(Ps[-1][0:2, 0:2], xs[-1][0:2], 4)
            ce = plot_cov_ellipse(Ps[-1][0:2, 0:2], xs[-1][0:2], 4)
            ca.set_alpha(0.2)
            ca.set_facecolor(CMAP(cl))
            ce.set_facecolor('none')
            ce.set_edgecolor(CMAP(cl))
            ce.set_linewidth(4)

        if r_values:
            plt.text(xs[-1][0]+20, xs[-1][1], '{0:.2f}'.format(rs[-1]), color=CMAP(cl), fontsize=16)

        if track_id:
            plt.text(xs[-1][0]+20, xs[-1][1]+20, str(id_), color=CMAP(cl), )


def plot_traces(targets, cseed=0, covellipse=True, max_back=None, **kwargs):
    """Plot all targets' traces."""
    for t in targets:
        plot_trace(t, t.id + cseed, covellipse, max_back, **kwargs)


def plot_cov_ellipse(cov, pos, nstd=2, **kwargs):
    """Plot confidence ellipse."""
    r1, r2, theta = cov_ellipse(cov, nstd)
    ellip = Ellipse(xy=pos, width=2*r1, height=2*r2, angle=theta, **kwargs)

    plt.gca().add_artist(ellip)
    return ellip


def plot_scan(reports, origin, covellipse=True, **kwargs):
    """Plot reports from scan."""
    options = {
        'marker': '+',
        'color': 'r',
        'linestyle': 'None'
    }
    options.update(kwargs)
    zs = [cf.ll2ne(r.z[0:2], origin) for r in reports]
    plt.plot([float(z[0]) for z in zs],
             [float(z[1]) for z in zs], **options)
    if covellipse:
        for r in reports:
            ca = plot_cov_ellipse(r.R[0:2, 0:2], cf.ll2ne(r.z[0:2], origin))
            ca.set_alpha(0.1)
            ca.set_facecolor(options['color'])


def plot_bbox(obj, cseed=0, **kwargs):
    """Plot bounding box."""
    id_ = getattr(obj, 'id', 0)
    options = {
        'alpha': 0.3,
        'color': CMAP(id_ + cseed)
    }
    options.update(kwargs)
    bbox = obj.bbox()
    plt.gca().add_patch(Rectangle(
        (bbox[0], bbox[2]), bbox[1] - bbox[0], bbox[3] - bbox[2],
        **options))
