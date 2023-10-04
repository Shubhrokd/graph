def text_to_batches(s, batch_size=2000):
    words = s.split()
    batches = []

    for i in range(0, len(words), batch_size):
        batch = " ".join(words[i : i + batch_size])
        batches.append(batch)

    return batches
