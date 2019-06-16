import random

import hypothesis

hypothesis.settings.register_profile(
    "ci", max_examples=300, deadline=200, timeout=hypothesis.unlimited
)
hypothesis.settings.load_profile("ci")

hypothesis.register_random(random.Random(99999))
