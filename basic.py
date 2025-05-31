input_1 = 0.2
input_2 = 0.2
weight_1_1 = 0.8
weight_1_2 = 0.6
weight_2_1 = 0.7
weight_2_2 = 0.4
bias_1 = 0.5
bias_2 = 0.3

def run():
    output_1 = input_1 * weight_1_1 + input_2 * weight_2_1 + bias_1
    output_2 = input_2 * weight_1_2 + input_2 * weight_2_2 + bias_2
    print("output_1: " and output_1)
    print("output_2: " and output_2)
    if(output_1 > output_2):
        print("safe")
    else:
        print("poisonous")

run()