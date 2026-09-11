# Aero-Thermo Tester formulas

## Dynamic pressure
\[
q = \frac{1}{2}\rho V^2
\]

## Modified Newtonian pressure coefficient
For each face normal \(\hat{n}_i\) and flow direction \(\hat{V}\):
\[
\mu_i = \max(0,\hat{n}_i \cdot (-\hat{V}))
\]
\[
C_{p,i} = C_{p,max}\mu_i^2
\]
where
\[
C_{p,max} = \frac{2}{\gamma M^2}\left[\left(\frac{(\gamma+1)^2M^2}{4\gamma M^2-2(\gamma-1)}\right)^{\frac{\gamma}{\gamma-1}}\left(\frac{1-\gamma+2\gamma M^2}{\gamma+1}\right)-1\right]
\]

## Pressure force per face
\[
\vec{F}_{p,i} = -p_i A_i \hat{n}_i, \quad p_i = qC_{p,i}
\]

## Skin friction drag (flat approximation)
\[
C_f = \frac{0.074}{Re_L^{1/5}},\quad Re_L = \frac{\rho VL}{\mu}
\]
\[
\vec{F}_{f,i} = -q C_f A_i \hat{V}
\]

## Surface heating
\[
T_0 = T_\infty\left(1+\frac{\gamma-1}{2}M^2\right)
\]
\[
T_r = T_\infty + r(T_0-T_\infty)
\]
\[
\dot{q}_i = h\left(T_r - T_{w,i}\right)
\]
