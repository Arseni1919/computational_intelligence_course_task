from CONSTANTS import *
import statistics
# '5_50_10_0point1_'
# '5_20_30_0point1_'
# '5_20_5_0point1_'
# 15_20_5_0point1_
# 15_200_5_0point1_
# 15_20_5_0point3_
# 15_100_5_0point3_
# 3_500_5_0point1_
add_to_name = '15_100_5_0point3_'
# links = ["results/SA.p", "results/ch.p", "results/greedy.p", "results/local_search.p",]
links = [
    f"results/{add_to_name}SA.p",
    f"results/{add_to_name}ch.p",
    f"results/{add_to_name}greedy.p",
    f"results/{add_to_name}local_search.p",
    f'results/{add_to_name}GA.p'
]

# links = ["results/SA.p", "results/ch.p", "results/greedy.p", "results/local_search.p","results/GA.p"]

for link in links:
    results = pickle.load(open(link, "rb"))
    graph = []
    x = []
    # for i in range(results.shape[0]):
    last_iteration_to_look_at = 20
    for i in range(min(last_iteration_to_look_at, results.shape[0])):
        graph.append(np.mean(results[i]))
        x.append(i)
    plt.plot(graph, label=link[len(f"results/{add_to_name}"):])

    i = min(last_iteration_to_look_at, results.shape[0]) - 1
    print('iteration: ', i, link, ':', '\n',
          'max:', max(results[i]), '\n',
          'min:', min(results[i]),'\n',
          'mean:', statistics.mean(results[i]),'\n',
          'sd:', statistics.stdev(results[i]), '\n',
          )

plt.legend()
plt.title('total rewards')
plt.show()
