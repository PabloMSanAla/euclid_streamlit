import streamlit as st
import pandas as pd
import os
import base64


# === SETTINGS ===
IMAGES_DIR = "/home/pmsa/code/euclid_streamlit/rgb/"  
IMAGE_SUFFIX = "_rgb-1.jpg"
IMAGE_PREFIX = "source_"

# === UPLOAD CSV ===
st.title("Evolution of disc breaks viewer\nSánchez-Alarcón et al. in prep.")


# csv_file = st.file_uploader("Upload CSV with OBJECT_ID column", type=["csv"])
csv_file = 'test.csv'

if csv_file is not None:
    df = pd.read_csv(csv_file)

    if "object_id" not in df.columns:
        st.error("CSV must contain 'OBJECT_ID'.")
    else:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found.")
        else:
            col = st.selectbox("Select column to sort/filter by:", numeric_cols)
            descending = st.toggle("Descending order", value=True)

            # === SLIDER ===
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            range_val = st.slider(
                f"Filter {col} values:",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                step=(max_val - min_val) / 100
            )

            # Filter & sort
            filtered = df[(df[col] >= range_val[0]) & (df[col] <= range_val[1])]
            filtered = filtered.sort_values(col, ascending=not descending).reset_index(drop=True)

            st.write(f"**Showing {len(filtered)} objects in range [{range_val[0]:.2f}, {range_val[1]:.2f}]**")

            # === INFINITE SCROLL ===
            batch_size = 32
            ncols = 4

            if 'batch' not in st.session_state:
                st.session_state.batch = batch_size

            topN = filtered.head(st.session_state.batch)

            cols = st.columns(ncols)  # 5 per row

            for idx, (_, row) in enumerate(topN.iterrows()):
                obj_id = str(row['object_id'])
                img_filename = f"{IMAGE_PREFIX}{obj_id}{IMAGE_SUFFIX}"
                img_path = os.path.join(IMAGES_DIR, img_filename)

                col_idx = idx % ncols
                if os.path.exists(img_path):
                    cols[col_idx].image(img_path, caption=f"{obj_id}\n{col}: {row[col]:.2f}", use_container_width=True)
                else:
                    cols[col_idx].write(f"Image not found: {img_filename}")

            # === Load more ===
            if st.session_state.batch < len(filtered):
                if st.button("Load more"):
                    st.session_state.batch += batch_size