from scipy import linalg as la
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.manifold.spectral_embedding_ import *


def gaussian_kernel(data1, data2, sigma):

    delta = np.matrix(abs(np.subtract(data1, data2)))
    squared_euclidean = (np.square(delta).sum(axis=1))
    result = np.exp(-squared_euclidean/(2*sigma**2))
    return result


def build_similarity_matrix(data_in, var):

    n_data = data_in.shape[0]
    result = np.matrix(np.full((n_data, n_data), 0, dtype=np.float))
    for i in range(0, n_data):
        for j in range(0, n_data):
            weight = gaussian_kernel(data_in[i, :], data_in[j, :], var)
            result[i, j] = weight
    return result


def build_degree_matrix(similarity_matrix):

    diag = np.array(similarity_matrix.sum(axis=1)).ravel()
    result = np.diag(diag)
    return result


def unnormalized_laplacian(sim_matrix, deg_matrix):

    result = deg_matrix - sim_matrix
    return result


def calculate_eigen_vectors(laplacian):

    e_vals, e_vecs = la.eigh(np.matrix(laplacian))
    ind = e_vals.argsort()[:e_vals.shape[0]]
    return e_vals, e_vecs, ind


def take_x_eigen_vectors(e_vecs, ind, laplacian, how_many):

    result = np.ndarray(shape=(laplacian.shape[0], 0))
    # print(result.shape)
    for i in range(1, how_many):
        cor_e_vec = np.transpose(np.matrix(e_vecs[:, np.asscalar(ind[i])]))
        result = np.concatenate((result, cor_e_vec), axis=1)
    return result


def k_means(x, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    return kmeans.fit(x).labels_


def spectral_clustering(df, n_clusters, affinity, gamma):

    graph_cluster = SpectralClustering(n_clusters=n_clusters, affinity=affinity, gamma=gamma)
    graph_result = graph_cluster.fit_predict(df)
    return graph_result


def test_laplacian(laplacian, vals, vectors, epsilon=0.000001):
    """Unit testing the Laplacian. We need to assert that the properties mentioned in Section 3.1 of the tutorial at
    <https://www.cs.cmu.edu/~aarti/Class/10701/readings/Luxburg06_TR.pdf> hold true. """

    num_vertices = laplacian.shape[0]

    # Sizes are as expected.
    assert laplacian.shape[0] == laplacian.shape[1] and laplacian.shape[0] == num_vertices

    # Property 2: L is symmetric.

    assert np.allclose(laplacian, laplacian.T, atol=epsilon)

    # Property 4: L has n non-negative, real-valued eigenvalues.
    # vals, vectors = np.linalg.eigh(L)
    assert all([vals[i].imag == 0 for i in range(num_vertices)]) and len(vals) == num_vertices

    # Property 3: The smallest eigenvalue of L is 0, the corresponding eigenvector is the constant one vector.
    assert vals.min() < epsilon

    # Recursively assert that all elements in a vector are equal to each other.
    first_vector = vectors[:, 0]  # Remember `np.linalg.eigh` returns eigenvectors as columns.
    print(first_vector)  # All elements are identical -> Constant one vector.
