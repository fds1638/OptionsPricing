# OptionsPricing

Repo doing options pricing following Wilmott et. al.

**To Run**

Run main.py, which will run all three solutions below.

**Purpose:**

Solve the Black-Scholes equation below in three different ways:

$$
\frac{\partial V}{\partial t}
+\frac{1}{2}\sigma^{2}S^{2}\frac{\partial^{2} V}{\partial S^{2}}
+rS\frac{\partial V}{\partial S}
-rV = 0$$

Solve for a European call option with exercise price $E$, which leads to the following initial and boundary conditions:

$$V(0, t) = 0$$

$$V(S, t) \rightarrow S - Ee^{r(T-t)} \text{  as  } S \rightarrow \infty$$

$$V(S, T) = max(0, S - E)$$

**Method 1: Closed form**

$$V(S,t) = N(d_{+})S-N(d_{-})Ee^{-r(T-t)}$$

where N is the standard normal cumulative distribution function and:

$$d_{+}=\frac{1}{\sigma\sqrt{T-t}}\[ln\(\frac{S_{t}}{E}\)+\( r+\frac{1}{2}\sigma^{2} \) (T-t) \] $$

$$d_{-} = d_{+} - \sigma\sqrt{T-t}$$

**Method 2: transform to heat equation and use forward Euler**

Use the following transformations:

$$S = Ee^{x}$$

$$\tau = \frac{\sigma^2}{2}(T-t)$$

$$u(x, \tau) = Ee^{\alpha x}e^{\beta \tau}V(S,t)$$

where:

$$\alpha = -\frac{1}{2}\left( \frac{2r}{\sigma^2}-1\right)$$

$$\beta = -\frac{1}{4}\left( \frac{2r}{\sigma^2}+1\right)^{2}$$

yields the following heat equation and boundary conditions:

$$u_{\tau}=u_{xx}$$

$$u(x,\tau) \rightarrow 0 \text{ as } \tau \rightarrow -\infty$$

$$u(x,\tau) \rightarrow e^{-\alpha x}e^{-\beta\tau}(e^{x}-e^{-2r\tau /\sigma^{2}}) \text{ as } \tau \rightarrow \infty$$

$$u(x, 0) = e^{-\alpha x}(e^{x}-1)$$

This system of equations is solved with forward Euler.

**Method 3: transform to heat equation and use backward Euler**

The same heat equation and initial and boundary condition system of equations is solved with backwards Euler.

**Result**

With $\sigma=0.1$, $r=0.05$, $E=50$, and exercise date at $T=50$:

[alt text](/closed_fe_be.png, raw=true)


