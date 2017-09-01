import os
import sys
import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn.utils as utils
import torch.optim as optim
import shutil
import random
import hyperparams
torch.manual_seed(hyperparams.seed_num)
random.seed(hyperparams.seed_num)

def train(train_iter, dev_iter, test_iter, model, args):
    if args.cuda:
        model.cuda()

    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.init_weight_decay)
    # optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=args.lr)

    steps = 0
    model_count = 0
    model.train()
    for epoch in range(1, args.epochs+1):
        print("## 第{} 轮迭代，共计迭代 {} 次 ！##".format(epoch, args.epochs))
        # the attr of shuffle in train_iter haved initialed True during data.Iterator.splits()
        for batch in train_iter:
            feature, target = batch.text, batch.label.data.sub_(1)
            target =autograd.Variable(target)
            if args.cuda:
                feature, target = feature.cuda(), target.cuda()

            optimizer.zero_grad()
            # model.zero_grad()
            model.hidden = model.init_hidden(args.lstm_num_layers, args.batch_size)
            if feature.size(1) != args.batch_size:
                model.hidden = model.init_hidden(args.lstm_num_layers, feature.size(1))
            logit = model(feature)
            # target values >=0   <=C - 1 (C = args.class_num)
            loss = F.cross_entropy(logit, target)
            loss.backward()
            # prevent grads boom
            # utils.clip_grad_norm(model.parameters(), args.max_norm)
            # the up line will make overfitting quickly, however, the line slow the overfitting,
            # so,the speed of overfitting depend on the max_norm size, more big, moe quickly
            if args.init_clip_max_norm is not None:
                # print("aaaa {} ".format(args.init_clip_max_norm))
                utils.clip_grad_norm(model.parameters(), max_norm=args.init_clip_max_norm)
            optimizer.step()

            steps += 1
            if steps % args.log_interval == 0:
                train_size = len(train_iter.dataset)
                corrects = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
                accuracy = float(corrects)/batch.batch_size * 100.0
                sys.stdout.write(
                    '\rBatch[{}/{}] - loss: {:.6f}  acc: {:.4f}%({}/{})'.format(steps,
                                                                            train_size,
                                                                             loss.data[0], 
                                                                             accuracy,
                                                                             corrects,
                                                                             batch.batch_size))
            if steps % args.test_interval == 0:
                eval(dev_iter, model, args)
            if steps % args.save_interval == 0:
                if not os.path.isdir(args.save_dir): os.makedirs(args.save_dir)
                save_prefix = os.path.join(args.save_dir, 'snapshot')
                save_path = '{}_steps{}.pt'.format(save_prefix, steps)
                torch.save(model, save_path)
                model_count += 1
                test_eval(test_iter, model, save_path, args, model_count)
    return model_count


def eval(data_iter, model, args):
    model.eval()
    corrects, avg_loss = 0, 0
    for batch in data_iter:
        feature, target = batch.text, batch.label
        feature.data.t_(), target.data.sub_(1)  # batch first, index align
        if args.cuda:
            feature, target = feature.cuda(), feature.cuda()

        model.hidden = model.init_hidden(args.lstm_num_layers, args.batch_size)
        if feature.size(1) != args.batch_size:
            model.hidden = model.init_hidden(args.lstm_num_layers, feature.size(1))
        logit = model(feature)
        loss = F.cross_entropy(logit, target, size_average=False)
        # scheduler.step(loss.data[0])

        avg_loss += loss.data[0]
        corrects += (torch.max(logit, 1)
                     [1].view(target.size()).data == target.data).sum()

    size = len(data_iter.dataset)
    avg_loss = loss.data[0]/size
    accuracy = float(corrects)/size * 100.0
    model.train()
    print('\nEvaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) \n'.format(avg_loss,
                                                                       accuracy,
                                                                       corrects,
                                                                       size))


def test_eval(data_iter, model, save_path, args, model_count):
    # print(save_path)
    model.eval()
    corrects, avg_loss = 0, 0
    for batch in data_iter:
        feature, target = batch.text, batch.label
        target.data.sub_(1)  # batch first, index align
        if args.cuda:
            feature, target = feature.cuda(), target.cuda()

        model.hidden = model.init_hidden(args.lstm_num_layers, args.batch_size)
        if feature.size(1) != args.batch_size:
            model.hidden = model.init_hidden(args.lstm_num_layers, feature.size(1))
        logit = model(feature)
        loss = F.cross_entropy(logit, target, size_average=False)

        avg_loss += loss.data[0]
        corrects += (torch.max(logit, 1)
                     [1].view(target.size()).data == target.data).sum()

    size = len(data_iter.dataset)
    avg_loss = loss.data[0]/size
    accuracy = float(corrects)/size * 100.0
    model.train()
    print('\nEvaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) \n'.format(avg_loss,
                                                                       accuracy,
                                                                       corrects,
                                                                       size))
    print("model_count {}".format(model_count))
    # test result
    if os.path.exists("./Test_Result.txt"):
        file = open("./Test_Result.txt", "a")
    else:
        file = open("./Test_Result.txt", "w")
    file.write("model " + save_path + "\n")
    file.write("Evaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) \n".format(avg_loss, accuracy, corrects, size))
    file.write("model_count {} \n".format(model_count))
    file.write("\n")
    file.close()
    shutil.copy("./Test_Result.txt", "./snapshot/" + args.mulu + "/Test_Result.txt")
    # whether to delete the model after test acc so that to save space
    if os.path.isfile(save_path) and args.rm_model is True:
        os.remove(save_path)
