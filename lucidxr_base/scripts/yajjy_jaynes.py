def train_fn():
    print('hey')


if __name__ == '__main__':
    import jaynes
    from jaynes.param_codec import serialize

    s = serialize(train_fn)
    print(s)
    exit()
