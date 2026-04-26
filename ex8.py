import math
from tabulate import tabulate

# ─────────────────────────────────────────────
#  Activation Functions
# ─────────────────────────────────────────────

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def tanh_fn(x):
    return math.tanh(x)

def threshold(x, theta=0.5):
    return 1 if x >= theta else 0

def activation_function(x, fn_type, theta=0.5, bipolar=False):
    """
    fn_type: 'sigmoid' | 'tanh' | 'threshold'
    For bipolar threshold: maps 0 → -1, 1 → 1
    """
    if fn_type == 'sigmoid':
        val = sigmoid(x)
    elif fn_type == 'tanh':
        val = tanh_fn(x)
    elif fn_type == 'threshold':
        val = threshold(x, theta)
        if bipolar:
            val = 1 if val == 1 else -1
    else:
        raise ValueError(f"Unknown activation function: {fn_type}")
    return val

# ─────────────────────────────────────────────
#  Data Initialisation
# ─────────────────────────────────────────────

def get_binary_data(n_inputs):
    """Generate all 2^n binary input combinations."""
    rows = 2 ** n_inputs
    data = []
    for i in range(rows):
        bits = [(i >> (n_inputs - 1 - j)) & 1 for j in range(n_inputs)]
        data.append(bits)
    return data

def get_bipolar_data(binary_data):
    """Convert binary {0,1} → bipolar {-1,+1}."""
    return [[1 if b == 1 else -1 for b in row] for row in binary_data]

def zeros():
    """Return a fresh weight/bias tuple of zeros."""
    return 0.0, 0.0, 0.0   # w1, w2, bias

# ─────────────────────────────────────────────
#  Dot Product
# ─────────────────────────────────────────────

def dot(inputs, weights, bias):
    """Compute weighted sum: w1*x1 + w2*x2 + bias."""
    return sum(x * w for x, w in zip(inputs, weights)) + bias

# ─────────────────────────────────────────────
#  Weight Update
# ─────────────────────────────────────────────

def update_weights(inputs, target, output, weights, bias, lr):
    """
    Delta rule: Δw_i = lr * (target - output) * x_i
                Δb   = lr * (target - output)
    Returns (dw_list, db, new_weights, new_bias)
    """
    error = target - output
    dw = [lr * error * x for x in inputs]
    db = lr * error
    new_w = [w + d for w, d in zip(weights, dw)]
    new_b = bias + db
    return dw, db, new_w, new_b

# ─────────────────────────────────────────────
#  Main Training Function
# ─────────────────────────────────────────────

def train_perceptron():
    print("=" * 70)
    print("   NEURAL NETWORK – PERCEPTRON TRAINER")
    print("=" * 70)

    # ── User Inputs ──────────────────────────────────────────────────────
    data_type = input("\nData type – enter 'binary' or 'bipolar': ").strip().lower()
    while data_type not in ('binary', 'bipolar'):
        data_type = input("  Invalid. Enter 'binary' or 'bipolar': ").strip().lower()
    is_bipolar = data_type == 'bipolar'

    n_inputs = int(input("Number of inputs (e.g. 2): ").strip())

    target_vals = []
    print(f"\nEnter target (desired) output for each of the {2**n_inputs} input combinations:")
    bin_data = get_binary_data(n_inputs)
    for row in bin_data:
        label = str(row)
        t = float(input(f"  Target for {label}: ").strip())
        target_vals.append(t)

    print("\nInitial weights (press Enter for 0):")
    init_weights = []
    for i in range(n_inputs):
        val = input(f"  w{i+1}: ").strip()
        init_weights.append(float(val) if val else 0.0)

    val = input("  Bias: ").strip()
    init_bias = float(val) if val else 0.0

    lr = float(input("Learning rate (α, e.g. 1): ").strip())
    epochs = int(input("Number of epochs: ").strip())

    fn_type = input("Activation function – 'sigmoid' / 'tanh' / 'threshold': ").strip().lower()
    while fn_type not in ('sigmoid', 'tanh', 'threshold'):
        fn_type = input("  Invalid. Choose 'sigmoid', 'tanh', or 'threshold': ").strip().lower()

    theta = 0.5
    if fn_type == 'threshold':
        val = input("Threshold θ (press Enter for 0.5): ").strip()
        theta = float(val) if val else 0.5

    # ── Data Preparation ─────────────────────────────────────────────────
    if is_bipolar:
        input_data = get_bipolar_data(bin_data)
    else:
        input_data = bin_data

    # ── Training Loop ─────────────────────────────────────────────────────
    w = list(init_weights)
    b = init_bias

    all_rows = []   # collected for the master table

    for epoch in range(1, epochs + 1):
        epoch_rows = []
        for idx, (inputs, target) in enumerate(zip(input_data, target_vals)):
            yin = dot(inputs, w, b)
            y   = activation_function(yin, fn_type, theta, is_bipolar)

            dw, db, new_w, new_b = update_weights(inputs, target, y, w, b, lr)

            row = {
                'Epoch': epoch,
                'X1'   : inputs[0],
                'X2'   : inputs[1] if n_inputs > 1 else '-',
                'YIN'  : round(yin, 4),
                'Y'    : round(y, 4),
            }
            for i, d in enumerate(dw):
                row[f'ΔW{i+1}'] = round(d, 4)
            row['ΔBias'] = round(db, 4)
            for i, nw in enumerate(new_w):
                row[f'W{i+1}(new)'] = round(nw, 4)
            row['Bias(new)'] = round(new_b, 4)

            epoch_rows.append(row)
            all_rows.append(row)

            w = new_w
            b = new_b

        # ── Per-epoch summary table ───────────────────────────────────────
        print(f"\n{'─'*70}")
        print(f"  EPOCH {epoch}")
        print(f"{'─'*70}")
        print(tabulate(
            [[r['Epoch'], r['X1'], r['X2'], r['YIN'], r['Y'],
              *[r[f'ΔW{i+1}'] for i in range(n_inputs)],
              r['ΔBias'],
              *[r[f'W{i+1}(new)'] for i in range(n_inputs)],
              r['Bias(new)']]
             for r in epoch_rows],
            headers=(
                ['Epoch', 'X1', 'X2', 'YIN', 'Y'] +
                [f'ΔW{i+1}' for i in range(n_inputs)] +
                ['ΔBias'] +
                [f'W{i+1}(new)' for i in range(n_inputs)] +
                ['Bias(new)']
            ),
            tablefmt='fancy_grid',
            numalign='center',
            stralign='center'
        ))

    # ── Final Weights ─────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print("  FINAL WEIGHTS & BIAS (after all epochs)")
    print(f"{'=' * 70}")
    final_rows = [[f'W{i+1}' for i in range(n_inputs)] + ['Bias'],
                  [round(w[i], 4) for i in range(n_inputs)] + [round(b, 4)]]
    print(tabulate(
        [final_rows[1]],
        headers=final_rows[0],
        tablefmt='fancy_grid',
        numalign='center'
    ))

    # ── Full Master Table ─────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print("  COMPLETE TRAINING TABLE (All Epochs)")
    print(f"{'=' * 70}")
    print(tabulate(
        [[r['Epoch'], r['X1'], r['X2'], r['YIN'], r['Y'],
          *[r[f'ΔW{i+1}'] for i in range(n_inputs)],
          r['ΔBias'],
          *[r[f'W{i+1}(new)'] for i in range(n_inputs)],
          r['Bias(new)']]
         for r in all_rows],
        headers=(
            ['Epoch', 'X1', 'X2', 'YIN', 'Y'] +
            [f'ΔW{i+1}' for i in range(n_inputs)] +
            ['ΔBias'] +
            [f'W{i+1}(new)' for i in range(n_inputs)] +
            ['Bias(new)']
        ),
        tablefmt='fancy_grid',
        numalign='center',
        stralign='center'
    ))

    print(f"\n✔ Training complete.  Final W = {[round(x,4) for x in w]}  |  Final Bias = {round(b,4)}\n")

# ─────────────────────────────────────────────
if __name__ == '__main__':
    train_perceptron()
