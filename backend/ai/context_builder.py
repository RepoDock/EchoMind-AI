class ContextBuilder:

    def build(self, results, include_source=True):

        context = ""

        for (
            chunk_id,
            file_id,
            score,
            chunk,
            file_name,
            page_number,
            *extra
        ) in results:

            if include_source:

                context += f"""
Source: {file_name}
Page: {page_number}

{chunk}

--------------------

"""

            else:

                context += f"""
Page: {page_number}

{chunk}

"""

        return context