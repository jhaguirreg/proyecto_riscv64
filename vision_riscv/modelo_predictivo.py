import numpy as np

# Capas de la red neuronal convolucional.
def conv2d(x, kernels, bias, stride=1):
    h, w, c = x.shape
    kh, kw, kc, out_c = kernels.shape
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1

    y = np.zeros((out_h, out_w, out_c), dtype=np.float32)

    for oh in range(out_h):
        for ow in range(out_w):
            patch = x[oh*stride : oh*stride+kh,
                       ow*stride : ow*stride+kw,
                       :]
            for oc in range(out_c):
                y[oh, ow, oc] = np.sum(patch * kernels[:, :, :, oc]) + bias[oc]
    return y

def maxpool(x, pool=2, stride=2):
    h, w, c = x.shape
    out_h = (h - pool) // stride + 1
    out_w = (w - pool) // stride + 1

    y = np.zeros((out_h, out_w, c), dtype=np.float32)

    for oh in range(out_h):
        for ow in range(out_w):
            patch = x[oh*stride : oh*stride+pool,
                       ow*stride : ow*stride+pool,
                       :]
            y[oh, ow, :] = np.max(patch, axis=(0,1))
    return y

def relu(x):
    return np.maximum(0, x)

def flatten(x):
    return x.reshape(-1)

def dense(x, W, b):
    return W.T @ x + b

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

def predict(im28x28, pesos):
    # Extraer pesos del modelo
    W1, b1, W2, b2, W3, b3, W4, b4, W5, b5 = pesos

    # Convertir imagen 28x28 a 28x28x1
    x = im28x28.astype(np.float32)
    x = x[..., np.newaxis]

    # Bloque 1
    x = relu(conv2d(x, W1, b1))
    x = maxpool(x)

    # Bloque 2
    x = relu(conv2d(x, W2, b2))
    x = maxpool(x)

    # Bloque 3
    x = relu(conv2d(x, W3, b3))

    # Flatten
    x = x.reshape(-1)

    # Dense 64
    x = relu(dense(x, W4, b4))

    # Dense 10
    logits = dense(x, W5, b5)

    # Softmax
    probs = softmax(logits)

    pred = np.argmax(probs)
    return pred, probs