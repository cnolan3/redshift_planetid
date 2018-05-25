import tf_lstm as lstm
import sys

m = lstm.Model(20)

if sys.argv[3] == 'train':
    lstm.train(m, 5, 3, 100, "data.txt", "labels.txt", "./saved")
else:
    x, y = lstm.load_test_data(sys.argv[1], sys.argv[2])

    lstm.run(m, 5, x, "./saved")
