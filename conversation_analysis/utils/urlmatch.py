# Adapted from https://gist.github.com/winzig/8894715

url_re = r"""
(?xi)
\b
(                                       # Capture 1: entire matched URL
  (?:
    https?:                             # URL protocol and colon
    (?:
      /{1,3}                            # 1-3 slashes
      |                                 #   or
      [a-z0-9%]                         # Single letter or digit or '%'
                                        # (Trying not to match e.g. "URI::Escape")
    )
    |                                   #   or
                                        # looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:[a-z]{2,13})
    /
  )
  (?:                                   # One or more:
    [^\s()<>{}\[\]]+                    # Run of non-space, non-()<>{}[]
    |                                   #   or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)                         # balanced parens, non-recursive: (…)
  )+
  (?:                                   # End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)                         # balanced parens, non-recursive: (…)
    |                                   #   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]      # not a space or one of these punct chars
  )
  |                                     # OR, the following to match naked domains:
  (?:\b
    (?<![@.])                           # not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:[a-z]{2,13})
    \b
    /?
    (?!@)                               # not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
    /                                   # nkraft: followed by a slash to avoid field or method accesses (e.g., Set.size)
  )
)
"""

