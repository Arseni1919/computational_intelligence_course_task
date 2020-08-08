from CONSTANTS import *

links = ["results/SA.p", "results/ch.p", "results/greedy.p", "results/local_search.p",]
links = ["results/5_100_0point1_SA.p", "results/5_100_0point1_ch.p",
         "results/5_100_0point1_greedy.p", "results/5_100_0point1_local_search.p",]

# links = ["results/SA.p", "results/ch.p", "results/greedy.p", "results/local_search.p","results/GA.p"]

for link in links:
    results = pickle.load(open(link, "rb"))
    graph = []
    for i in range(results.shape[0]):
        graph.append(np.mean(results[i]))
        print(results[i])
    plt.plot(graph, label=link)
    print(f'{link}:{graph}')

plt.legend()
plt.title('total rewards')
plt.show()
