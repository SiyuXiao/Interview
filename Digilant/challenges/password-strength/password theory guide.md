Based on data science to design the password strength:

Using $\mathcal{X_i}$ to represent the password charater of index $i$, the probability of a password$(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$ is $p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$

When I use$p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$measure a password strength，the smaller of $p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$，the stronger the password will be，the greater of $p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$, the weaker the password will be. 

In real situation，we can use the probability of $p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$ to classify multiple thresholds. We can classify the strength thresholds as follows:

very weak：$p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l}) \geq \lambda_{\mathcal{1}}$

weak：$\lambda_{\mathcal{1}} > p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l}) \geq \lambda_{\mathcal{2}}$

medium：$\lambda_{\mathcal{2}} > p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l}) \geq \lambda_{\mathcal{3}}$

strong：$\lambda_{\mathcal{3}} > p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l}) \geq \lambda_{\mathcal{4}}$

very strong：$\lambda_{\mathcal{4}} > p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$



I can fit a probability based on Maxsium Likelyhood Estimation and Information Theory, the following link is a method to estimate  $p(\mathcal{X_1}, \mathcal{X_2}, \dots, \mathcal{X_l})$ :

https://ieeexplore.ieee.org/document/8005906

