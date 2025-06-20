#%%

import pandas as pd
import os
import glob

files = glob.glob('rgb/*.pdf')

object_ids = [os.path.basename(f).replace('_rgb.pdf', '').replace('source_', '') for f in files]
object_ids = [int(c) for c in object_ids]
# %%
