import os
import sys
from sklearn.cluster import KMeans
import pandas as pd
from keras.datasets import mnist
from sklearn.mixture import GMM
from scipy.spatial.distance import cdist
# Generate some data
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from matplotlib.patches import Ellipse

X, y_true = make_blobs(n_samples=400, centers=4,cluster_std=0.60, random_state=0)
X = X[:, ::-1] # flip axes for better plotting

#The 5 Clustering Algorithms Data Scientists Need to Know
#website:https://towardsdatascience.com/the-5-clustering-algorithms-data-scientists-need-to-know-a36d136ef68




#Gaussian Mixture Models
#website:https://jakevdp.github.io/PythonDataScienceHandbook/05.12-gaussian-mixtures.html
def gmm_cluster(n_components_no,array_data):
    gmm = GMM(n_components=n_components_no).fit(array_data)
    labels = gmm.predict(array_data)
    plt.scatter(array_data[:, 0], array_data[:, 1], c=labels, s=40, cmap='viridis')
    probs = gmm.predict_proba(array_data)
    print(probs[:5].round(3))

def draw_ellipse(position, covariance, ax=None, **kwargs):
    """Draw an ellipse with a given position and covariance"""
    ax = ax or plt.gca()
    
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    
    # Draw the Ellipse
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))
        
def plot_gmm(gmm, X, label=True, ax=None):
    ax = ax or plt.gca()
    labels = gmm.fit(X).predict(X)
    if label:
        ax.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis', zorder=2)
    else:
        ax.scatter(X[:, 0], X[:, 1], s=40, zorder=2)
    ax.axis('equal')
    
    w_factor = 0.2 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covars_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor)

def main():
    gmm_cluster(4,X)
    print("not tested...")

if __name__=="__main__":
    main()
