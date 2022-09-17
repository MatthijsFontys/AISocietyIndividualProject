import random
import neurolab as nl


class GeneticNeurolab:

    @staticmethod
    def show_info(net):
        for layer in net.layers:
            GeneticNeurolab.show_layer_info(layer)

    @staticmethod
    def show_layer_info(layer):
        print(layer.np['w'])
        #print(layer.np['b'])

    @staticmethod
    def cross_over(net_a, net_b):
        offspring = net_a.copy()
        for layer_index in range(len(offspring.layers)):
            layer = offspring.layers[layer_index]
            shape = layer.np['w'].shape
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if random.random() < 0.5:
                        layer.np['w'][i, j] = net_b.layers[layer_index].np['w'][i, j]
                        layer.np['w'][i, j] = GeneticNeurolab.get_mutated_value(layer.np['w'][i, j])
            for b in range(layer.np['b'].shape[0]):
                if random.random() < 0.5 and False:
                    layer.np['b'][b] = net_b.layers[layer_index].np['b'][b]
                layer.np['b'][b] = GeneticNeurolab.get_mutated_value(layer.np['b'][b])
        # print('Parent A')
        # GeneticNeurolab.show_layer_info(net_a.layers[0])
        # print('Parent B')
        # GeneticNeurolab.show_layer_info(net_b.layers[0])
        # print('Child')
        # GeneticNeurolab.show_layer_info(offspring.layers[0])
        return offspring


    @staticmethod
    def get_mutated_value(value):
        sine = [1, -1]
        if random.random() < 0.03:
            delta = random.random() * random.choice(sine)
            value += delta
        return value
