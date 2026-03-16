
class StandardCompressor:

    def clean(self, text):
        text = text.strip()
        text = text.replace("please kindly", "")
        text = text.replace("in order to", "to")

        lines = []
        seen = set()

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            if line in seen:
                continue

            seen.add(line)
            lines.append(line)

        return "\n".join(lines)

    def compress(self, messages):

        out = []

        for m in messages:

            text = m["content"]

            text = self.clean(text)

            out.append({
                "role": m["role"],
                "content": text,
            })

        return out
