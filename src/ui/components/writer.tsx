import { useArtifact } from "../utils/use-artifact";
import { useEffect, useRef, useState } from "react";
import { LoaderIcon } from "lucide-react";

export function Writer(props: {
    title?: string;
    content?: string;
    description?: string;
    isGenerating: boolean;
}) {
    const [Artifact, { open, setOpen, setContext }] = useArtifact<{
        writer?: { selected?: string };
    }>();

    const [content, setContent] = useState(props.content ?? "");
    useEffect(() => setContent(props.content ?? ""), [props.content]);

    const prevOpened = useRef(false);
    const shouldAutoOpen = !open && content.length > 0 && props.isGenerating;
    useEffect(() => {
        if (shouldAutoOpen && !prevOpened.current) {
            prevOpened.current = true;
            setOpen(true);
        }
    }, [shouldAutoOpen, setOpen]);

    return (
        <>
            <div
                onClick={() => setOpen(!open)}
                className="border p-4 rounded-lg cursor-pointer"
            >
                <p className="font-medium">{props.title}</p>
                <p className="text-sm text-gray-500">{props.description}</p>

                {props.isGenerating && (
                    <p className="flex items-center gap-2">
                        <LoaderIcon className="animate-spin" />
                        <span>Generating...</span>
                    </p>
                )}
            </div>

            <Artifact title={props.title}>
                <textarea
                    className="absolute inset-0 w-full h-full p-4 outline-none"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    onSelect={(e) => {
                        const selectedText = e.currentTarget.value.substring(
                            e.currentTarget.selectionStart,
                            e.currentTarget.selectionEnd,
                        );
                        setContext((prevContext) => ({
                            ...prevContext,
                            writer: { ...prevContext?.writer, selected: selectedText },
                        }));
                    }}
                />
            </Artifact>
        </>
    );
}