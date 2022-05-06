# 联邦学习安全聚合器
# Federated Learning Secure Aggregator

import os
import shutil
import torch
import numpy as np
import logging

from classification import trainer


class SecAgg:

    def __init__(self, port, n_frames, num_clients, split_type):
        self.n_frames = n_frames
        self.init_logger()
        self.port = port
        self.num_clients = num_clients
        self.split_type = split_type
        self.client_id = 'client_{}'.format(self.port)
        self.client_models_folder = 'secure_aggregator/client_models'
        self.init_model()

    def init_logger(self):
        l_filename = 'logs/fl_sec_aggr.log'
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(l_filename),
                logging.StreamHandler()
            ]
        )

    def init_model(self):
        self.trainer = trainer.SecAggTrainer(self.port,
                                             self.n_frames,
                                             self.num_clients,
                                             self.client_id,
                                             self.split_type)

    def load_models(self):
        logging.info('Loading client models...')
        arr = []
        for root, dirs, files in os.walk(self.client_models_folder,
                                         topdown=True):
            for name in files:
                if name.endswith('model.tar'):
                    fn = os.path.join(root, name)
                    data = torch.load(fn)
                    # arr.append(np.load(fn, allow_pickle=True))
                    arr.append(data)
                    logging.info('Loaded {}'.format(fn))
        models = np.array(arr)
        logging.info('Done')
        return models

    @staticmethod
    def average_weights(models):
        logging.info('Averaging weights...')

        avg_model = models[0].copy()
        for k in avg_model:
            tmp = [w[k].cpu() for w in models]
            # avg_model[k] = np.average(tmp)
            avg_model[k] = np.true_divide(sum(tmp), len(tmp))

        logging.info('\tDone. Averaged {} models'.format(len(models)))
        return avg_model

    def aggregate_models(self):
        model_weights = self.load_models()
        self.weights = self.average_weights(model_weights)
        avg_weights = self.weights
        self.trainer.update_model(avg_weights)

    def get_model_filename(self):
        return self.trainer.get_best_model_path()

    def save_model(self):
        self.trainer.save_model()

    def delete_client_models(self):
        logging.info('Deleting client models...')
        for filename in os.listdir(self.client_models_folder):
            if not filename.endswith('.tar'):
                continue
            file_path = os.path.join(self.client_models_folder, filename)
            logging.info('\tDeleting {}'.format(file_path))
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.info('Failed to delete %s. Reason: %s' % (file_path, e))
        logging.info('\tDone')

    def test(self):
        test_result = self.trainer.test()
        return test_result

