from src.agents.library_assistant import LibraryAssistant


def main():
    assistant = LibraryAssistant()

    print(assistant.graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
