# Baum Welch Algorithm
- 最適な出力確率と遷移確率のパラメータを推定する
- HMMのパラメタに使える

# 理論
## logsumexp
<img src="https://latex.codecogs.com/gif.latex?\mathrm{logsumexp}&space;\left(\left\{&space;p_k&space;\right&space;\}_{k=1}^{K}&space;\right&space;)&space;\equiv&space;\mathrm{log}\left&space;(&space;\sum&space;_{k=1}^{K}&space;\exp&space;p_{k}&space;\right&space;)" />

- 単純にexpの足し算を計算するとアンダーフローを起こすので、先に指数部分を計算しておくことでアンダーフローを防ぎやすくなる

## Jensenの不等式
<img src="https://latex.codecogs.com/gif.latex?f&space;\left&space;(&space;\int&space;y\left&space;(&space;x&space;\right&space;)p\left&space;(&space;x&space;\right&space;)dx&space;\right&space;)&space;\geq&space;\int&space;f\left&space;(&space;y\left&space;(&space;x&space;\right&space;)&space;\right&space;)p\left&space;(&space;x&space;\right&space;)dx"/>

- fが上に凸のときに成り立つ

## EMアルゴリズム

<img src="https://latex.codecogs.com/gif.latex?\textrm{E&space;step:}&space;\hat{q}\left&space;(&space;z&space;\right&space;)&space;=&space;\underset{q\left&space;(&space;z&space;\right&space;)}{\mathrm{argmax}}&space;F\left&space;(&space;q\left&space;(&space;z&space;\right&space;),\theta&space;\right&space;)">

<img src="https://latex.codecogs.com/gif.latex?\textrm{M&space;step:}&space;\hat{\theta&space;}&space;=&space;\underset{\theta}{\mathrm{argmax}}&space;F\left&space;(&space;q\left&space;(&space;z&space;\right&space;),\theta&space;\right&space;)\\">

- それぞれ、片方を固定してそのときの関数が最大となるような変数を求め、交互に更新していく
- 最終的にこの手法によって対数尤度は単調増加していくが、それが大域最適解である保証はない

# 実行
- 今回はサイコロが本物か、偽物の2種類の隠れ状態とする
- 上から順に実行することで、イテレーションごとの確率が出力される
    - 停止はしないので、気が済んだらやめる
- 確率がansと近いことを確認する
- 最後にviterviアルゴリズムで隠れ状態列を出力し、精度を確かめる

# Todo
- [ ] HMMの場合のEMの計算過程
- [ ] 事後デコーディング