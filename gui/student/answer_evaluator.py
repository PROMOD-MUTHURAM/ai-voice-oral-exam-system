



# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if text is None:

        return ""

    text = str(
        text
    ).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()





class AnswerEvaluator:

    def __init__(self):
        self.model = None

    def load_model(self):

        if self.model is not None:
            return True

        try:
            from sentence_transformers import SentenceTransformer

            print("Loading semantic similarity model...")

            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            print("Semantic similarity model loaded.")

            return True

        except Exception as e:

            print("Could not load similarity model:")
            print(e)

            return False

    def similarity(
        self,
        expected_answer,
        student_answer
    ):

        expected_answer = normalize_text(
            expected_answer
        )

        student_answer = normalize_text(
            student_answer
        )

        if not student_answer:
            return 0.0

        if not expected_answer:
            return 0.0

        if expected_answer == student_answer:
            return 100.0

        if not self.load_model():
            return 0.0

        try:

            from sentence_transformers.util import cos_sim

            embeddings = self.model.encode(
                [
                    expected_answer,
                    student_answer
                ],
                convert_to_tensor=True
            )

            score = cos_sim(
                embeddings[0],
                embeddings[1]
            ).item()

            score = max(
                0.0,
                min(1.0, score)
            )

            return round(
                score * 100,
                2
            )

        except Exception as e:

            print("Similarity calculation error:")
            print(e)

            return 0.0
