# Baum Welch Algorithm
- 最適な出力確率と遷移確率のパラメータを推定する
- HMMのパラメタに使える

# 理論
### logsumexp
<img src="https://latex.codecogs.com/gif.latex?\mathrm{logsumexp}&space;\left(\left\{&space;p_k&space;\right&space;\}_{k=1}^{K}&space;\right&space;)&space;\equiv&space;\mathrm{log}\left&space;(&space;\sum&space;_{k=1}^{K}&space;\exp&space;p_{k}&space;\right&space;)" />