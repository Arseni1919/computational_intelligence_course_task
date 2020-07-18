from CONSTANTS import *

links = ["results/SA.p",]

for link in links:
    results = pickle.load(open(link, "rb"))
    graph = []
    for i in range(results.shape[0]):
        graph.append(np.mean(results[i]))
    plt.plot(graph, label=link)

plt.legend()
plt.title('total rewards')
plt.show()
