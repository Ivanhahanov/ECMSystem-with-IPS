rule TextExample
{
    strings:
        $text_string = "foobar"

    condition:
        $text_string
}