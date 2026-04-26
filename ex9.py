from fractions import Fraction
from tabulate import tabulate

# ─────────────────────────────────────────────────────────────────────────────
#  UTILITY
# ─────────────────────────────────────────────────────────────────────────────

def sep(char="═", n=70):
    print(char * n)

def header(title):
    sep()
    print(f"   {title}")
    sep()

def step(num, desc):
    print(f"\n  STEP {num}: {desc}")
    print("  " + "─" * 60)

def fmt(v):
    """Display a probability as decimal (4dp) and fraction."""
    try:
        f = Fraction(v).limit_denominator(1000)
        return f"{v:.4f}  ({f})"
    except Exception:
        return f"{v:.4f}"

# ─────────────────────────────────────────────────────────────────────────────
#  INPUT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_float(prompt, lo=0.0, hi=1.0):
    while True:
        try:
            v = float(input(prompt).strip())
            if lo <= v <= hi:
                return v
            print(f"    ✘ Value must be between {lo} and {hi}. Try again.")
        except ValueError:
            print("    ✘ Invalid number. Try again.")

def get_int(prompt, lo=1):
    while True:
        try:
            v = int(input(prompt).strip())
            if v >= lo:
                return v
            print(f"    ✘ Value must be ≥ {lo}. Try again.")
        except ValueError:
            print("    ✘ Invalid integer. Try again.")

def get_events(label="event"):
    n = get_int(f"\n  How many {label}s? ")
    events = []
    for i in range(n):
        name = input(f"  Name of {label} {i+1}: ").strip() or f"{label.upper()}{i+1}"
        events.append(name)
    return events

# ─────────────────────────────────────────────────────────────────────────────
#  1. MARGINAL PROBABILITY
# ─────────────────────────────────────────────────────────────────────────────

def marginal_probability():
    header("MARGINAL PROBABILITY  P(A)")
    print("""
  Definition : P(A) = (Number of favourable outcomes) / (Total outcomes)
               OR entered directly as a probability value.
  Formula    : P(A) = n(A) / n(S)
""")

    mode = input("  Enter probabilities (1) directly  OR  (2) via counts? [1/2]: ").strip()

    events = get_events("event")
    probs  = {}

    if mode == "2":
        step(1, "Enter outcome counts for each event")
        counts = {}
        for e in events:
            counts[e] = get_int(f"    Count of outcomes for '{e}': ")
        total = sum(counts.values())

        step(2, "Compute total sample space")
        print(f"    Total outcomes  n(S) = {' + '.join(str(counts[e]) for e in events)} = {total}")

        step(3, "Calculate P(A) for each event")
        rows = []
        for e in events:
            p = counts[e] / total
            probs[e] = p
            rows.append([e, counts[e], total, fmt(p)])
            print(f"    P({e}) = {counts[e]} / {total} = {fmt(p)}")
        print()
        print(tabulate(rows, headers=["Event", "n(A)", "n(S)", "P(A)"], tablefmt="fancy_grid"))

    else:
        step(1, "Enter probability for each event")
        for e in events:
            probs[e] = get_float(f"    P({e}) = ")

        step(2, "Verify probabilities sum to 1")
        total = sum(probs.values())
        print(f"    Σ P = {' + '.join(f'P({e})' for e in events)} = {total:.4f}")
        if abs(total - 1.0) < 1e-6:
            print("    ✔ Probabilities sum to 1 — valid distribution.")
        else:
            print(f"    ⚠ Warning: Probabilities sum to {total:.4f}, not 1.")

        step(3, "Summary table")
        rows = [[e, fmt(probs[e])] for e in events]
        print(tabulate(rows, headers=["Event", "P(A)"], tablefmt="fancy_grid"))

    step(4, "Complementary probabilities  P(A') = 1 − P(A)")
    rows2 = []
    for e in events:
        comp = 1 - probs[e]
        rows2.append([e, fmt(probs[e]), fmt(comp)])
        print(f"    P({e}') = 1 − {probs[e]:.4f} = {fmt(comp)}")
    print()
    print(tabulate(rows2, headers=["Event", "P(A)", "P(A')"], tablefmt="fancy_grid"))

    print("\n  ✔ Marginal Probability calculation complete.\n")

# ─────────────────────────────────────────────────────────────────────────────
#  2. JOINT PROBABILITY
# ─────────────────────────────────────────────────────────────────────────────

def joint_probability():
    header("JOINT PROBABILITY  P(A ∩ B)")
    print("""
  Definition : Probability that BOTH events A and B occur simultaneously.

  Two methods:
    (a) Independent events : P(A ∩ B) = P(A) × P(B)
    (b) Dependent  events  : P(A ∩ B) = P(A) × P(B|A)
    (c) From joint table   : enter the joint frequency table directly
""")

    choice = input("  Choose method — (a) Independent  (b) Dependent  (c) Table: ").strip().lower()

    # ── (a) Independent ──────────────────────────────────────────────────────
    if choice == 'a':
        step(1, "Enter marginal probabilities")
        pa = get_float("    P(A) = ")
        pb = get_float("    P(B) = ")

        step(2, "Verify independence assumption")
        print("    For independent events: P(A ∩ B) = P(A) × P(B)")
        print(f"    P(A) = {fmt(pa)}")
        print(f"    P(B) = {fmt(pb)}")

        step(3, "Calculate joint probability")
        joint = pa * pb
        print(f"    P(A ∩ B) = P(A) × P(B)")
        print(f"             = {pa:.4f} × {pb:.4f}")
        print(f"             = {fmt(joint)}")

        step(4, "Summary")
        rows = [["P(A)", fmt(pa)], ["P(B)", fmt(pb)], ["P(A ∩ B)", fmt(joint)]]
        print(tabulate(rows, headers=["Quantity", "Value"], tablefmt="fancy_grid"))

    # ── (b) Dependent ─────────────────────────────────────────────────────────
    elif choice == 'b':
        step(1, "Enter marginal and conditional probabilities")
        pa  = get_float("    P(A)   = ")
        pba = get_float("    P(B|A) = ")

        step(2, "Apply multiplication rule")
        print("    P(A ∩ B) = P(A) × P(B|A)")
        print(f"             = {pa:.4f} × {pba:.4f}")
        joint = pa * pba
        print(f"             = {fmt(joint)}")

        step(3, "Cross-check: P(B ∩ A) = P(B) × P(A|B)")
        pb  = get_float("    P(B)   = (enter to cross-check) ")
        pab = joint / pb if pb > 0 else 0
        print(f"    P(A|B) = P(A ∩ B) / P(B) = {joint:.4f} / {pb:.4f} = {fmt(pab)}")
        print(f"    P(B) × P(A|B) = {pb:.4f} × {pab:.4f} = {fmt(pb*pab)}")
        print("    ✔ Both routes give same P(A ∩ B)." if abs(pb*pab - joint) < 1e-6 else "    ✔ Values computed.")

        step(4, "Summary")
        rows = [["P(A)", fmt(pa)], ["P(B)", fmt(pb)],
                ["P(B|A)", fmt(pba)], ["P(A|B)", fmt(pab)], ["P(A ∩ B)", fmt(joint)]]
        print(tabulate(rows, headers=["Quantity", "Value"], tablefmt="fancy_grid"))

    # ── (c) Table ─────────────────────────────────────────────────────────────
    else:
        step(1, "Define events")
        row_events = get_events("row event (A)")
        col_events = get_events("column event (B)")

        step(2, "Enter joint frequency counts")
        counts = {}
        for r in row_events:
            for c in col_events:
                counts[(r, c)] = get_int(f"    Count for ({r} ∩ {c}): ")

        total = sum(counts.values())

        step(3, "Compute total")
        print(f"    Grand total n = {total}")

        step(4, "Build joint probability table")
        table = []
        for r in row_events:
            row_data = [r]
            for c in col_events:
                row_data.append(fmt(counts[(r, c)] / total))
            table.append(row_data)

        print(tabulate(table, headers=[""] + col_events, tablefmt="fancy_grid"))

        step(5, "Marginal probabilities from table")
        print("    Row marginals  P(A):")
        for r in row_events:
            p = sum(counts[(r, c)] for c in col_events) / total
            print(f"      P({r}) = {fmt(p)}")
        print("    Column marginals  P(B):")
        for c in col_events:
            p = sum(counts[(r, c)] for r in row_events) / total
            print(f"      P({c}) = {fmt(p)}")

    print("\n  ✔ Joint Probability calculation complete.\n")

# ─────────────────────────────────────────────────────────────────────────────
#  3. CONDITIONAL PROBABILITY
# ─────────────────────────────────────────────────────────────────────────────

def conditional_probability():
    header("CONDITIONAL PROBABILITY  P(A|B)")
    print("""
  Definition : Probability of A given that B has already occurred.
  Formula    : P(A|B) = P(A ∩ B) / P(B)   where P(B) > 0
""")

    choice = input("  Do you know (1) P(A∩B) and P(B)  OR  (2) enter a joint table? [1/2]: ").strip()

    if choice == "2":
        # ── From table ────────────────────────────────────────────────────────
        step(1, "Define events")
        row_events = get_events("row event (A)")
        col_events = get_events("column event (B)")

        step(2, "Enter joint frequency counts")
        counts = {}
        for r in row_events:
            for c in col_events:
                counts[(r, c)] = get_int(f"    Count for ({r} ∩ {c}): ")

        total = sum(counts.values())

        step(3, "Joint probability table  P(Ai ∩ Bj)")
        table = []
        for r in row_events:
            row_data = [r]
            for c in col_events:
                row_data.append(round(counts[(r,c)]/total, 4))
            table.append(row_data)
        print(tabulate(table, headers=[""] + col_events, tablefmt="fancy_grid"))

        step(4, "Marginal probabilities")
        row_marg = {r: sum(counts[(r,c)] for c in col_events)/total for r in row_events}
        col_marg = {c: sum(counts[(r,c)] for r in row_events)/total for c in col_events}
        print("    P(A) row marginals:")
        for r in row_events:
            print(f"      P({r}) = {fmt(row_marg[r])}")
        print("    P(B) column marginals:")
        for c in col_events:
            print(f"      P({c}) = {fmt(col_marg[c])}")

        step(5, "Conditional probabilities  P(A|B) = P(A∩B) / P(B)")
        cond_rows = []
        for r in row_events:
            for c in col_events:
                joint = counts[(r,c)] / total
                pb    = col_marg[c]
                cond  = joint / pb if pb > 0 else 0
                cond_rows.append([f"P({r}|{c})",
                                   fmt(joint), fmt(pb), fmt(cond)])
                print(f"    P({r}|{c}) = P({r}∩{c}) / P({c}) = {joint:.4f} / {pb:.4f} = {fmt(cond)}")
        print()
        print(tabulate(cond_rows,
                       headers=["Conditional", "P(A∩B)", "P(B)", "P(A|B)"],
                       tablefmt="fancy_grid"))

    else:
        # ── Direct input ──────────────────────────────────────────────────────
        step(1, "Enter known probabilities")
        pab = get_float("    P(A ∩ B) = ")
        pb  = get_float("    P(B)     = ", lo=1e-9)

        step(2, "Apply the formula")
        print("    P(A|B) = P(A ∩ B) / P(B)")
        print(f"           = {pab:.4f} / {pb:.4f}")
        result = pab / pb
        print(f"           = {fmt(result)}")

        step(3, "Reverse conditional  P(B|A)")
        pa = get_float("    P(A)     = ", lo=1e-9)
        pba = pab / pa
        print(f"    P(B|A) = P(A ∩ B) / P(A) = {pab:.4f} / {pa:.4f} = {fmt(pba)}")

        step(4, "Summary")
        rows = [["P(A)", fmt(pa)], ["P(B)", fmt(pb)],
                ["P(A ∩ B)", fmt(pab)],
                ["P(A|B)", fmt(result)], ["P(B|A)", fmt(pba)]]
        print(tabulate(rows, headers=["Quantity", "Value"], tablefmt="fancy_grid"))

    print("\n  ✔ Conditional Probability calculation complete.\n")

# ─────────────────────────────────────────────────────────────────────────────
#  4. BAYES' THEOREM
# ─────────────────────────────────────────────────────────────────────────────

def bayes_theorem():
    header("BAYES' THEOREM  P(Ai|B)")
    print("""
  Formula:
              P(Ai) × P(B|Ai)
  P(Ai|B) = ──────────────────────────────
              Σ [ P(Aj) × P(B|Aj) ]

  Where:
    P(Ai)    = Prior probability of hypothesis Ai
    P(B|Ai)  = Likelihood: probability of evidence B given Ai
    P(Ai|B)  = Posterior probability of Ai given evidence B
    Σ [...]  = Total probability (normalisation constant)
""")

    step(1, "Define hypotheses (causes / classes)")
    n = get_int("    How many hypotheses? ")
    hyp = []
    for i in range(n):
        name = input(f"    Name of hypothesis {i+1} (e.g. H1): ").strip() or f"H{i+1}"
        hyp.append(name)

    step(2, "Enter prior probabilities  P(Hi)")
    priors = {}
    for h in hyp:
        priors[h] = get_float(f"    P({h}) = ")

    total_prior = sum(priors.values())
    print(f"\n    Σ P(Hi) = {total_prior:.4f}", end="")
    if abs(total_prior - 1.0) < 1e-6:
        print("  ✔ Valid (sums to 1)")
    else:
        print(f"  ⚠ Warning: does not sum to 1")

    step(3, "Enter likelihoods  P(B|Hi)  — one evidence event B")
    likelihoods = {}
    for h in hyp:
        likelihoods[h] = get_float(f"    P(B|{h}) = ")

    step(4, "Calculate joint probabilities  P(Hi) × P(B|Hi)")
    joints = {}
    joint_rows = []
    for h in hyp:
        j = priors[h] * likelihoods[h]
        joints[h] = j
        joint_rows.append([h, fmt(priors[h]), fmt(likelihoods[h]),
                           f"{priors[h]:.4f} × {likelihoods[h]:.4f}", fmt(j)])
        print(f"    P({h}) × P(B|{h}) = {priors[h]:.4f} × {likelihoods[h]:.4f} = {fmt(j)}")

    print()
    print(tabulate(joint_rows,
                   headers=["Hi", "P(Hi)", "P(B|Hi)", "Calculation", "Joint"],
                   tablefmt="fancy_grid"))

    step(5, "Calculate total probability  P(B) = Σ P(Hi) × P(B|Hi)")
    pb = sum(joints.values())
    terms = " + ".join(f"{joints[h]:.4f}" for h in hyp)
    print(f"    P(B) = {terms}")
    print(f"         = {fmt(pb)}")

    step(6, "Calculate posterior probabilities  P(Hi|B)")
    posteriors = {}
    post_rows  = []
    for h in hyp:
        post = joints[h] / pb if pb > 0 else 0
        posteriors[h] = post
        post_rows.append([h, fmt(joints[h]), fmt(pb),
                          f"{joints[h]:.4f} / {pb:.4f}", fmt(post)])
        print(f"    P({h}|B) = {joints[h]:.4f} / {pb:.4f} = {fmt(post)}")

    print()
    print(tabulate(post_rows,
                   headers=["Hi", "P(Hi)×P(B|Hi)", "P(B)", "Calculation", "P(Hi|B)"],
                   tablefmt="fancy_grid"))

    step(7, "Verification  Σ P(Hi|B) should = 1")
    total_post = sum(posteriors.values())
    print(f"    Σ P(Hi|B) = {total_post:.6f}", end="")
    print("  ✔" if abs(total_post - 1.0) < 1e-5 else "  ⚠ Check inputs")

    step(8, "Final summary table")
    summary = []
    for h in hyp:
        summary.append([h, fmt(priors[h]), fmt(likelihoods[h]),
                        fmt(joints[h]), fmt(pb), fmt(posteriors[h])])
    print(tabulate(summary,
                   headers=["Hi", "P(Hi) Prior", "P(B|Hi) Likelihood",
                             "Joint", "P(B) Evidence", "P(Hi|B) Posterior"],
                   tablefmt="fancy_grid"))

    # Most probable hypothesis
    best = max(posteriors, key=posteriors.get)
    print(f"\n  ★ Most probable hypothesis: {best}  with P({best}|B) = {fmt(posteriors[best])}\n")
    print("  ✔ Bayes' Theorem calculation complete.\n")

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

def menu():
    while True:
        sep("═")
        print("   PROBABILITY CALCULATOR — MAIN MENU")
        sep("═")
        print("""
   1.  Marginal Probability       P(A)
   2.  Joint Probability          P(A ∩ B)
   3.  Conditional Probability    P(A|B)
   4.  Bayes' Theorem             P(Hi|B)
   0.  Exit
""")
        sep("─")
        choice = input("   Enter choice [0-4]: ").strip()
        print()

        if   choice == '1': marginal_probability()
        elif choice == '2': joint_probability()
        elif choice == '3': conditional_probability()
        elif choice == '4': bayes_theorem()
        elif choice == '0':
            print("  Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter 0–4.\n")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    menu()
