# OptionsPricing

Repo doing options pricing following Wilmott et. al.

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

$$V(S,t) = N(d_{+})S_{t}-N(d_{-})Ee^{-r(T-t)}$$

where N is the standard normal cumulative distribution function and:

$$d_{+}=\frac{1}{\sigma\sqrt{T-t}}\[ln\(\frac{S_{t}}{E}\)+\( r+\frac{1}{2}\sigma^{2} \) (T-t) \] $$

$$d_{-} = d_{+} - \sigma\sqrt{T-t}$$

**Method 2: transform to head equation and use forward Euler**


**Method 3: transform to head equation and use backward Euler**
