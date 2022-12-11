class PlantumlParser:
    @staticmethod
    def flattenPlantumlString(string: str) -> str:
        string = string.replace("{", "\n{")
        string = '\n'.join([line.strip()
                            for line in string.splitlines()
                            if "'" not in line  # removing comments
                            and line != ""])   # removing empty lines
        return string
