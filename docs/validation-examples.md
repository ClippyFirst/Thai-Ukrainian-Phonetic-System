# Core validation examples

The tone engine is tested against the following structural cases:

| Structure | Expected tone |
|---|---|
| mid + live + no mark | mid |
| mid + dead + no mark | low |
| high + live + no mark | rising |
| high + dead + no mark | low |
| low + live + no mark | mid |
| low + dead + short + no mark | high |
| low + dead + long + no mark | falling |
| mid + mai ek | low |
| high + mai ek | low |
| low + mai ek | falling |
| mid + mai tho | falling |
| high + mai tho | falling |
| low + mai tho | high |
| mid + mai tri | high |
| mid + mai chattawa | rising |
