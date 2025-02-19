import math

def value_w_binary_tree(S:float, vol:float, r:float, K:float, T:float, num_steps:int) -> float:
    # initialize parameters
    vec = [0 for _ in range(num_steps+1)]
    dt = T/num_steps
    discount = math.exp(-r*dt)
    temp1 = math.exp( (r + vol*vol) *dt )
    temp2 = 0.5 * (discount + temp1)
    u = temp2 + math.sqrt(temp2*temp2 - 1)
    d = 1/u
    p = ( math.exp(r*dt) - d) / ( u - d)

    # calculate asset values going forward in time
    vec[0] = S
    for n in range(1, num_steps+1):
        for j in range(n, 0, -1):
            vec[j] = u * vec[j-1]
        vec[0] *= d

    # apply payoff, in this case a call option
    for j in range(num_steps+1):
        vec[j] = max(0, vec[j] - K)

    # calculate option values going backwards in time
    for n in range(num_steps, 0, -1):
        old_vec = vec.copy()
        for j in range(n-1, -1, -1):
            vec[j] = ( p * old_vec[j+1] + (1-p)*old_vec[j] ) * discount

    return vec[0]


if __name__=='__main__':
    print(value_w_binary_tree(100, 0.2, 0.1, 100, 4/12, 4))