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


## Related Resources

- [**awesome-streamlit**](https://github.com/MarcSkovMadsen/awesome-streamlit): List of Awesome Streamlit Apps
- [**Streamlit App Gallery**](https://www.streamlit.io/gallery): Official Streamlit Apps Gallery
- [**Best-of**](https://best-of.org): Best-of lists with Python and other languages
- [**Best-of Streamlit**](https://github.com/jrieke/best-of-streamlit): Best-of list of Streamlit Apps