import random
import datetime

from gensim.models.word2vec import LineSentence, Word2Vec


def train_embedding(
    windowed_dataset,
    window_days,
    embedding_dim,
    train_idx,
):
    person_ixs, time_ixs, _ = windowed_dataset.feature_tensor.coords
    data_filename = "wtv_data_window_{}d.txt".format(window_days)
    f = open(data_filename, "a")
    c = list(zip(person_ixs, time_ixs))
    c_unique = sorted(list(set(c)))
    until = None
    s = []
    last_p = None 
    for i, (p_ix, t_ix) in enumerate(c_unique):
        if p_ix != last_p:
            until = None
            last_p = p_ix
        t = time_ixs 
        t = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        if until is None or t > until:
            if s:
                for _ in range(5):
                    f.write(' '.join(
                        str(w) for w in random.sample(s, len(s))
                    ))
                    f.write('\n')
            s = []
            until = t + datetime.timedelta(days=window_days)
        s += windowed_dataset.matrix_windowed[
            p_ix, t_ix, :
        ].coords[0].tolist()
        if i % 500000 == 0 :
            print('Wrote {} of {} to file'.format(i, len(c_unique)))
    f.close()

    sentences = LineSentence(data_filename)
    model = Word2Vec(min_count=0, size=embedding_dim, workers=10)
    model.build_vocab(sentences)
    n_epochs = 20
    model.train(sentences, total_examples=model.corpus_count, epochs=n_epochs)
    model.save("wtv_data_window_{}d_20epochs_model".format(window_days))
    model.wv.save("wtv_data_window_{}d_20epochs_wv".format(window_days))
    return "wtv_data_window_{}d_20epochs_wv".format(window_days)
