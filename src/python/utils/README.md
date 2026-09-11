# utils

Shared helpers: loading `config/settings.yaml`, unit conversions, and (Phase
7) the thin `.mat` file I/O layer that talks to `src/matlab/` via
`scipy.io.savemat`/`loadmat`. Keep MATLAB-specific glue code isolated here
rather than scattered through `simulation/` or `analysis/`.
