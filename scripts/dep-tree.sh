#!/bin/bash
# Shows the full dependency tree for all tickets, organized by epic

set -e

echo "=== FULL DEPENDENCY TREE ==="
echo ""
echo "Legend: [✓]=closed [→]=in_progress [ ]=open"
echo "        ↳ = depends on"
echo ""

TICKETS_DIR=".tickets"

if [ ! -d "$TICKETS_DIR" ]; then
    echo "Error: $TICKETS_DIR directory not found"
    exit 1
fi

for ticket in "$TICKETS_DIR"/*.md; do
    [ -e "$ticket" ] || continue
    id=$(basename "$ticket" .md)
    # Extract frontmatter fields
    status=$(grep "^status:" "$ticket" | cut -d' ' -f2)
    type=$(grep "^type:" "$ticket" | cut -d' ' -f2)
    parent=$(grep "^parent:" "$ticket" | cut -d' ' -f2)
    deps=$(grep "^deps:" "$ticket" | sed 's/deps: \[//' | sed 's/\]//' | tr -d ' ')
    # Get title (first # heading after frontmatter)
    title=$(sed -n '/^---$/,/^---$/!p' "$ticket" | grep "^# " | head -1 | sed 's/^# //')

    echo "$id|$status|$type|$parent|$deps|$title"
done | sort | awk -F'|' '
{
    id=$1; status=$2; type=$3; parent=$4; deps=$5; title=$6

    if (status == "closed") sym="[✓]"
    else if (status == "in_progress") sym="[→]"
    else sym="[ ]"

    # Store for later
    data[id] = sym " " id ": " title
    parents[id] = parent
    dependencies[id] = deps
    types[id] = type
    all_ids[id] = 1
}
END {
    # Print epics first, then their children
    for (id in all_ids) {
        if (types[id] == "epic") {
            print ""
            print data[id]
            # Find children
            for (child in parents) {
                if (parents[child] == id) {
                    printf "    %s", data[child]
                    if (dependencies[child] != "") {
                        printf "\n        ↳ %s", dependencies[child]
                    }
                    print ""
                }
            }
        }
    }
}
'
