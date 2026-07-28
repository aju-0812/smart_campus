import ast

def analyze_models(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
        
    models = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Check if it inherits from Base
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
            if 'Base' in bases or any(base != 'Exception' for base in bases):
                fields = []
                for child in node.body:
                    if isinstance(child, ast.Assign):
                        for target in child.targets:
                            if isinstance(target, ast.Name):
                                # Just get a string representation of the value
                                val_str = ast.unparse(child.value)
                                if 'Column' in val_str or 'relationship' in val_str:
                                    fields.append(f"{target.id}: {val_str}")
                if fields:
                    models[node.name] = fields
                    
    for model, fields in models.items():
        print(f"Model: {model}")
        for field in fields:
            print(f"  {field}")
        print()

if __name__ == "__main__":
    analyze_models("d:/smart campus/backend/app/models/models.py")
