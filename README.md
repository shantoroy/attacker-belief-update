# Adversarial-Belief-Update
This app can fingerprint Operating Systems using Bayes Net and Machine \
Learning as well as can simulate an Attacker's Intuition (Belief Update) \
inside a compromised network


## Primary Features: 
1. Real-life OS Fingerprinting using:
    * Bayes Network-based Knowledge Base
    * Multi-Class Classification Algorithms
2. Simulated Visualization of Node belief updates
3. Simulation of the updated belief for all nodes in a network

## Setup
### Run without docker
simply run using the following command
```
$ streamlit run main.py
```

### Run using docker
First, build the container using the `Dockerfile`
```
$ docker build -f Dockerfile -t app:belief-update .
```

Then run the container image using the following code
```
$ docker run -p 8501:8501 app:belief-update
```