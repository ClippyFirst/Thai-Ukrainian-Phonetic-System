# Ukrainian target integration

The canonical Ukrainian target is ClippyFirst/Ukrainian-Phonetic-Inventory.

This repository does not duplicate the full Ukrainian inventory. It stores a small reproducible feature-vector adapter in data/ua_target_vectors.csv so the pipeline is executable independently.

The feature dimensions and weight philosophy follow the target repository's public feature model. The local adapter is an integration snapshot and should eventually be generated from a versioned release of the canonical repository.

The output is a candidate set. It is not an assertion that the first candidate is the only correct Ukrainian rendering.
