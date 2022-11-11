# Intermediate language functions

The functions should be considered as follow:

```mermaid
classDiagram
    class Function {
        +Type return_type
        +String name
        +List~Variable~ arguments
        +repr() String
    }
```
