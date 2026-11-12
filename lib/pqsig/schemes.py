"""Scheme grouping: family, NIST level, distinct size classes."""
import pandas as pd

FAMS = (("ML-DSA", "ML-DSA"), ("Falcon", "Falcon/FN-DSA"), ("SLH_DSA", "SLH-DSA"), ("MAYO", "MAYO"), ("OV", "UOV"),
        ("SNOVA", "SNOVA"), ("cross", "CROSS"), ("mqom", "MQOM"), ("Ed25519", "classical"), ("ECDSA", "classical"))


def family(n):
    for pre, g in FAMS:
        if n.startswith(pre):
            return g
    return "other"


def add_classes(df):
    """df needs scheme, claimed_nist_level, length_public_key, sig_declared. Adds family, class_id, class_members, is_rep."""
    df = df.copy()
    df["family"] = df.scheme.map(family)
    df["class_key"] = list(zip(df.family, df.claimed_nist_level, df.length_public_key, df.sig_declared))
    df["class_id"] = df.class_key.map({k: i for i, k in enumerate(dict.fromkeys(sorted(df.class_key)))})
    df["class_members"] = df.groupby("class_id").scheme.transform("count")
    rep = df.assign(l=df.scheme.str.len()).sort_values(["class_id", "l", "scheme"]).groupby("class_id").head(1).scheme
    df["is_rep"] = df.scheme.isin(set(rep))
    df["variant_note"] = df.scheme.map(lambda n: "padded" if "padded" in n else "")
    return df.drop(columns="class_key")


def lowest_level(df):
    """Rows of the lowest claimed level available in each family."""
    m = df.groupby("family").claimed_nist_level.transform("min")
    return df[df.claimed_nist_level == m]
