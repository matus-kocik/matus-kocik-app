document.addEventListener("DOMContentLoaded", () => {
    const treeButton = document.getElementById("tree-button");
    const timelineButton = document.getElementById("timeline-button");

    const treeView = document.getElementById("tree-view");
    const timelineView = document.getElementById("timeline-view");

    const treeContainer = document.getElementById("economics-tree");
    const timelineContainer = document.getElementById("economics-timeline");

    // =========================================================
    // DETAIL ELEMENTS
    // =========================================================

    const nodeDetail = document.getElementById("node-detail");
    const nodeDetailType = document.getElementById("node-detail-type");
    const nodeDetailName = document.getElementById("node-detail-name");

    const nodeDetailTemporal = document.getElementById(
        "node-detail-temporal",
    );

    const nodeDetailYearFromWrapper = document.getElementById(
        "node-detail-year-from-wrapper",
    );
    const nodeDetailYearFrom = document.getElementById(
        "node-detail-year-from",
    );

    const nodeDetailYearToWrapper = document.getElementById(
        "node-detail-year-to-wrapper",
    );
    const nodeDetailYearTo = document.getElementById(
        "node-detail-year-to",
    );

    const nodeDetailPeriodWrapper = document.getElementById(
        "node-detail-period-wrapper",
    );
    const nodeDetailPeriod = document.getElementById(
        "node-detail-period",
    );

    const connectionDetailData = document.getElementById(
        "connection-detail-data",
    );
    const connectionDetailType = document.getElementById(
        "connection-detail-type",
    );
    const connectionDetailSource = document.getElementById(
        "connection-detail-source",
    );
    const connectionDetailTarget = document.getElementById(
        "connection-detail-target",
    );

    const nodeDetailShortDescriptionWrapper = document.getElementById(
        "node-detail-short-description-wrapper",
    );
    const nodeDetailShortDescription = document.getElementById(
        "node-detail-short-description",
    );

    const nodeDetailDescriptionWrapper = document.getElementById(
        "node-detail-description-wrapper",
    );
    const nodeDetailDescriptionLabel = document.getElementById(
        "node-detail-description-label",
    );
    const nodeDetailDescription = document.getElementById(
        "node-detail-description",
    );

    const nodeDetailClose = document.getElementById("node-detail-close");

    const nodesDataElement = document.getElementById(
        "rodokmen-nodes-data",
    );
    const connectionsDataElement = document.getElementById(
        "rodokmen-connections-data",
    );

    if (
        !treeButton ||
        !timelineButton ||
        !treeView ||
        !timelineView ||
        !treeContainer ||
        !timelineContainer ||
        !nodeDetail ||
        !nodeDetailType ||
        !nodeDetailName ||
        !nodeDetailTemporal ||
        !nodeDetailYearFromWrapper ||
        !nodeDetailYearFrom ||
        !nodeDetailYearToWrapper ||
        !nodeDetailYearTo ||
        !nodeDetailPeriodWrapper ||
        !nodeDetailPeriod ||
        !connectionDetailData ||
        !connectionDetailType ||
        !connectionDetailSource ||
        !connectionDetailTarget ||
        !nodeDetailShortDescriptionWrapper ||
        !nodeDetailShortDescription ||
        !nodeDetailDescriptionWrapper ||
        !nodeDetailDescriptionLabel ||
        !nodeDetailDescription ||
        !nodeDetailClose ||
        !nodesDataElement ||
        !connectionsDataElement
    ) {
        return;
    }

    // =========================================================
    // DJANGO DATA
    // =========================================================

    const djangoNodes = JSON.parse(nodesDataElement.textContent);
    const djangoConnections = JSON.parse(
        connectionsDataElement.textContent,
    );

    // =========================================================
    // NODE TYPES
    // =========================================================

    const nodeTypeLabels = {
        person: "Osobnosť",
        school: "Ekonomická škola",
        theory: "Teória / smer",
        concept: "Pojem / koncept",
        work: "Dielo",
        event: "Udalosť",
    };

    const timelineGroupIds = {
        school: 1,
        theory: 2,
        concept: 3,
        person: 4,
        work: 5,
        event: 6,
    };

    // =========================================================
    // HELPERS
    // =========================================================

    const hasValue = (value) => {
        if (value === null || value === undefined) {
            return false;
        }

        if (typeof value === "string") {
            return value.trim() !== "";
        }

        return true;
    };

    const formatHistoricalYear = (year) => {
        if (year === null || year === undefined) {
            return "";
        }

        if (year < 0) {
            return `${Math.abs(year)} pred n. l.`;
        }

        return `${year}`;
    };

    const createNodePeriod = (node) => {
        if (node.period_label && node.period_label.trim()) {
            return node.period_label.trim();
        }

        if (node.year_from === null && node.year_to === null) {
            return "";
        }

        if (
            node.year_from !== null &&
            node.year_to !== null &&
            node.year_from !== node.year_to
        ) {
            return `${formatHistoricalYear(node.year_from)} – ${formatHistoricalYear(
                node.year_to,
            )}`;
        }

        if (node.year_from !== null) {
            return formatHistoricalYear(node.year_from);
        }

        return formatHistoricalYear(node.year_to);
    };

    const createNodeLabel = (node) => {
        const period = createNodePeriod(node);

        if (!period) {
            return node.name;
        }

        return `${node.name}\n${period}`;
    };

    const getDjangoNode = (nodeId) => {
        return djangoNodes.find((node) => node.id === nodeId);
    };

    const getDjangoConnection = (connectionId) => {
        return djangoConnections.find(
            (connection) => connection.id === connectionId,
        );
    };

    const createHistoricalDate = (year) => {
        if (year === null || year === undefined) {
            return null;
        }

        const date = new Date(0);

        date.setUTCFullYear(year, 0, 1);
        date.setUTCHours(0, 0, 0, 0);

        return date;
    };

    const setDetailValue = (wrapper, element, value) => {
        if (hasValue(value)) {
            element.textContent = value;
            wrapper.classList.remove("hidden");
            return true;
        }

        element.textContent = "";
        wrapper.classList.add("hidden");

        return false;
    };

    const resetDetail = () => {
        nodeDetailType.textContent = "";
        nodeDetailName.textContent = "";

        nodeDetailYearFrom.textContent = "";
        nodeDetailYearTo.textContent = "";
        nodeDetailPeriod.textContent = "";

        nodeDetailYearFromWrapper.classList.add("hidden");
        nodeDetailYearToWrapper.classList.add("hidden");
        nodeDetailPeriodWrapper.classList.add("hidden");
        nodeDetailTemporal.classList.add("hidden");

        connectionDetailType.textContent = "";
        connectionDetailSource.textContent = "";
        connectionDetailTarget.textContent = "";
        connectionDetailData.classList.add("hidden");

        nodeDetailShortDescription.textContent = "";
        nodeDetailShortDescriptionWrapper.classList.add("hidden");

        nodeDetailDescription.textContent = "";
        nodeDetailDescriptionWrapper.classList.add("hidden");

        nodeDetailDescriptionLabel.textContent = "Detailný popis";
    };

    // =========================================================
    // NODE DETAIL
    // =========================================================

    const openNodeDetail = (nodeId) => {
        const node = getDjangoNode(nodeId);

        if (!node) {
            return;
        }

        resetDetail();

        nodeDetailType.textContent =
            node.node_type_display ||
            nodeTypeLabels[node.node_type] ||
            node.node_type;

        nodeDetailName.textContent = node.name;

        const hasYearFrom = setDetailValue(
            nodeDetailYearFromWrapper,
            nodeDetailYearFrom,
            formatHistoricalYear(node.year_from),
        );

        const hasYearTo = setDetailValue(
            nodeDetailYearToWrapper,
            nodeDetailYearTo,
            formatHistoricalYear(node.year_to),
        );

        const hasPeriod = setDetailValue(
            nodeDetailPeriodWrapper,
            nodeDetailPeriod,
            node.period_label,
        );

        if (hasYearFrom || hasYearTo || hasPeriod) {
            nodeDetailTemporal.classList.remove("hidden");
        }

        setDetailValue(
            nodeDetailShortDescriptionWrapper,
            nodeDetailShortDescription,
            node.short_description,
        );

        setDetailValue(
            nodeDetailDescriptionWrapper,
            nodeDetailDescription,
            node.description,
        );

        nodeDetailDescriptionLabel.textContent = "Detailný popis";

        nodeDetail.classList.remove("hidden");
    };

    // =========================================================
    // CONNECTION DETAIL
    // =========================================================

    const openConnectionDetail = (connectionId) => {
        const connection = getDjangoConnection(connectionId);

        if (!connection) {
            return;
        }

        const sourceNode = getDjangoNode(connection.source);
        const targetNode = getDjangoNode(connection.target);

        if (!sourceNode || !targetNode) {
            return;
        }

        resetDetail();

        nodeDetailType.textContent = "Prepojenie";

        nodeDetailName.textContent =
            `${sourceNode.name} → ${targetNode.name}`;

        connectionDetailType.textContent =
            connection.connection_type_display ||
            connection.connection_type ||
            "";

        connectionDetailSource.textContent = sourceNode.name;
        connectionDetailTarget.textContent = targetNode.name;

        connectionDetailData.classList.remove("hidden");

        if (hasValue(connection.description)) {
            nodeDetailDescription.textContent =
                connection.description;

            nodeDetailDescriptionLabel.textContent =
                "Popis prepojenia";

            nodeDetailDescriptionWrapper.classList.remove("hidden");
        }

        nodeDetail.classList.remove("hidden");
    };

    // =========================================================
    // VIS-NETWORK DATA
    // =========================================================

    const nodes = new vis.DataSet(
        djangoNodes.map((node) => ({
            id: node.id,
            label: createNodeLabel(node),
            group: node.node_type,
        })),
    );

    const edges = new vis.DataSet(
        djangoConnections.map((connection) => ({
            id: connection.id,
            from: connection.source,
            to: connection.target,
            label: connection.connection_type_display,
        })),
    );

    // =========================================================
    // NETWORK OPTIONS
    // =========================================================

    const networkOptions = {
        autoResize: true,

        layout: {
            hierarchical: {
                enabled: true,
                direction: "UD",
                sortMethod: "directed",
                levelSeparation: 130,
                nodeSpacing: 190,
                treeSpacing: 240,
                blockShifting: true,
                edgeMinimization: true,
                parentCentralization: true,
            },
        },

        physics: {
            enabled: false,
        },

        interaction: {
            hover: true,

            navigationButtons: true,

            keyboard: {
                enabled: true,
                bindToWindow: false,
            },

            zoomView: false,
            dragView: true,
            dragNodes: false,
            multiselect: false,
            selectable: true,
        },

        nodes: {
            shape: "box",

            widthConstraint: {
                minimum: 150,
                maximum: 220,
            },

            borderWidth: 2,
            borderWidthSelected: 3,

            margin: {
                top: 16,
                right: 20,
                bottom: 16,
                left: 20,
            },

            font: {
                face: "Arial",
                size: 16,
                color: "#252525",
            },

            shapeProperties: {
                borderRadius: 14,
            },

            shadow: {
                enabled: true,
                color: "rgba(0, 0, 0, 0.08)",
                size: 8,
                x: 0,
                y: 3,
            },

            chosen: {
                node: true,
                label: true,
            },
        },

        edges: {
            width: 1.5,

            arrows: {
                to: {
                    enabled: true,
                    scaleFactor: 0.7,
                },
            },

            color: {
                color: "#B7BDC3",
                highlight: "#4E8BC9",
                hover: "#4E8BC9",
                inherit: false,
            },

            font: {
                face: "Arial",
                size: 11,
                color: "#776B60",
                align: "middle",
                background: "#FFFFFF",
                strokeWidth: 0,
            },

            smooth: {
                enabled: true,
                type: "cubicBezier",
                forceDirection: "vertical",
                roundness: 0.35,
            },

            selectionWidth: 2,
            hoverWidth: 2,
        },

        groups: {
            person: {
                color: {
                    background: "#FFF1E5",
                    border: "#F2A15F",

                    highlight: {
                        background: "#FFE8D4",
                        border: "#F2A15F",
                    },

                    hover: {
                        background: "#FFE8D4",
                        border: "#F2A15F",
                    },
                },

                font: {
                    color: "#F2A15F",
                    size: 16,
                },
            },

            school: {
                color: {
                    background: "#E5F6F7",
                    border: "#66B7C2",

                    highlight: {
                        background: "#D9F1F3",
                        border: "#66B7C2",
                    },

                    hover: {
                        background: "#D9F1F3",
                        border: "#66B7C2",
                    },
                },

                font: {
                    color: "#66B7C2",
                    size: 16,
                },
            },

            theory: {
                color: {
                    background: "#E7F0F8",
                    border: "#4E8BC9",

                    highlight: {
                        background: "#DCECF8",
                        border: "#4E8BC9",
                    },

                    hover: {
                        background: "#DCECF8",
                        border: "#4E8BC9",
                    },
                },

                font: {
                    color: "#4E8BC9",
                    size: 16,
                },
            },

            concept: {
                color: {
                    background: "#F2ECFA",
                    border: "#9673C9",

                    highlight: {
                        background: "#E8DDF6",
                        border: "#9673C9",
                    },

                    hover: {
                        background: "#E8DDF6",
                        border: "#9673C9",
                    },
                },

                font: {
                    color: "#9673C9",
                    size: 16,
                },
            },

            work: {
                color: {
                    background: "#F8EAF2",
                    border: "#D88CB5",

                    highlight: {
                        background: "#F3DCE9",
                        border: "#D88CB5",
                    },

                    hover: {
                        background: "#F3DCE9",
                        border: "#D88CB5",
                    },
                },

                font: {
                    color: "#D88CB5",
                    size: 16,
                },
            },

            event: {
                color: {
                    background: "#FCEAE7",
                    border: "#F27C73",

                    highlight: {
                        background: "#F9DDD9",
                        border: "#F27C73",
                    },

                    hover: {
                        background: "#F9DDD9",
                        border: "#F27C73",
                    },
                },

                font: {
                    color: "#F27C73",
                    size: 16,
                },
            },
        },
    };

    // =========================================================
    // NETWORK
    // =========================================================

    const network = new vis.Network(
        treeContainer,
        {
            nodes: nodes,
            edges: edges,
        },
        networkOptions,
    );

    // =========================================================
    // NETWORK INITIAL VIEW
    // =========================================================

    network.once("afterDrawing", () => {
        if (nodes.length === 0) {
            return;
        }

        network.fit({
            animation: false,
        });

        const fittedScale = network.getScale();

        if (fittedScale < 0.9) {
            network.moveTo({
                scale: 0.9,
                animation: false,
            });
        }
    });

    // =========================================================
    // NETWORK EVENTS
    // =========================================================

    network.on("click", (params) => {
        if (params.nodes.length === 1) {
            openNodeDetail(params.nodes[0]);
            return;
        }

        if (params.edges.length === 1) {
            openConnectionDetail(params.edges[0]);
        }
    });

    network.on("doubleClick", (params) => {
        if (params.nodes.length !== 1) {
            return;
        }

        const nodeId = params.nodes[0];

        network.focus(nodeId, {
            scale: 1.25,

            animation: {
                duration: 400,
                easingFunction: "easeInOutQuad",
            },
        });
    });

    // =========================================================
    // TIMELINE GROUPS
    // =========================================================

    const timelineGroups = new vis.DataSet([
        {
            id: timelineGroupIds.school,
            content: "Ekonomické školy",
            order: 1,
        },
        {
            id: timelineGroupIds.theory,
            content: "Teórie / smery",
            order: 2,
        },
        {
            id: timelineGroupIds.concept,
            content: "Pojmy / koncepty",
            order: 3,
        },
        {
            id: timelineGroupIds.person,
            content: "Osobnosti",
            order: 4,
        },
        {
            id: timelineGroupIds.work,
            content: "Diela",
            order: 5,
        },
        {
            id: timelineGroupIds.event,
            content: "Udalosti",
            order: 6,
        },
    ]);

    // =========================================================
    // TIMELINE DATA
    // =========================================================

    const timelineItemsData = djangoNodes
        .filter(
            (node) =>
                node.year_from !== null ||
                node.year_to !== null,
        )
        .map((node) => {
            const startYear =
                node.year_from !== null
                    ? node.year_from
                    : node.year_to;

            const endYear =
                node.year_to !== null
                    ? node.year_to
                    : node.year_from;

            const item = {
                id: node.id,
                content: node.name,
                start: createHistoricalDate(startYear),
                group: timelineGroupIds[node.node_type],
                className: `timeline-${node.node_type}`,
                title: `${node.name}${createNodePeriod(node)
                        ? ` — ${createNodePeriod(node)}`
                        : ""
                    }`,
            };

            if (
                startYear !== null &&
                endYear !== null &&
                startYear !== endYear
            ) {
                item.end = createHistoricalDate(endYear + 1);
                item.type = "range";
            } else {
                item.type = "box";
            }

            return item;
        });

    const timelineItems = new vis.DataSet(timelineItemsData);

    // =========================================================
    // TIMELINE OPTIONS
    // =========================================================

    const timelineOptions = {
        height: "500px",

        orientation: {
            axis: "bottom",
            item: "top",
        },

        stack: true,
        stackSubgroups: true,

        horizontalScroll: true,
        verticalScroll: true,
        zoomKey: "ctrlKey",

        zoomMin: 1000 * 60 * 60 * 24 * 365 * 10,
        zoomMax: 1000 * 60 * 60 * 24 * 365 * 1000,

        selectable: true,
        multiselect: false,

        editable: false,
        moveable: true,
        zoomable: true,

        showCurrentTime: false,

        groupOrder: "order",

        margin: {
            axis: 20,

            item: {
                horizontal: 10,
                vertical: 10,
            },
        },

        tooltip: {
            followMouse: true,
            overflowMethod: "cap",
        },
    };

    // =========================================================
    // TIMELINE
    // =========================================================

    let timeline = null;

    const createTimeline = () => {
        if (timeline) {
            return;
        }

        timeline = new vis.Timeline(
            timelineContainer,
            timelineItems,
            timelineGroups,
            timelineOptions,
        );

        // =====================================================
        // TIMELINE EVENTS
        // =====================================================

        timeline.on("select", (properties) => {
            if (properties.items.length !== 1) {
                return;
            }

            openNodeDetail(properties.items[0]);
        });

        timeline.on("doubleClick", (properties) => {
            if (!properties.item) {
                return;
            }

            timeline.focus(properties.item, {
                animation: {
                    duration: 400,
                    easingFunction: "easeInOutQuad",
                },
            });
        });

        if (timelineItems.length > 0) {
            timeline.fit({
                animation: false,
            });
        }
    };

    // =========================================================
    // VIEW SWITCHER
    // =========================================================

    treeButton.addEventListener("click", () => {
        treeView.classList.remove("hidden");
        timelineView.classList.add("hidden");

        treeButton.classList.remove("btn-secondary");
        treeButton.classList.add("btn-primary");

        timelineButton.classList.remove("btn-primary");
        timelineButton.classList.add("btn-secondary");

        requestAnimationFrame(() => {
            network.redraw();
        });
    });

    timelineButton.addEventListener("click", () => {
        treeView.classList.add("hidden");
        timelineView.classList.remove("hidden");

        timelineButton.classList.remove("btn-secondary");
        timelineButton.classList.add("btn-primary");

        treeButton.classList.remove("btn-primary");
        treeButton.classList.add("btn-secondary");

        requestAnimationFrame(() => {
            if (!timeline) {
                createTimeline();
                return;
            }

            timeline.redraw();
        });
    });

    // =========================================================
    // CLOSE DETAIL
    // =========================================================

    const closeNodeDetail = () => {
        nodeDetail.classList.add("hidden");

        network.unselectAll();

        if (timeline) {
            timeline.setSelection([]);
        }
    };

    nodeDetailClose.addEventListener("click", closeNodeDetail);
});