"""
=========================================================
EMIDAF Framework v1.0
EMIX - Mixed Methods Integration Engine
=========================================================
"""

from __future__ import annotations

from .sources import (
    MixedMethodSource,
    SourceRegistry,
)
from .integration import (
    IntegrationLink,
    IntegrationManager,
    IntegrationCandidate,
    IntegrationCandidateGenerator,
    IntegrationCandidateManager,
    CandidateToLinkConverter,
)
from .joint_display import (
    JointDisplayRow,
    JointDisplayManager,
)
from .inference import (
    MetaInference,
    MetaInferenceManager,
)
from .summary import MixedMethodsSummary
from .session import EMIXSession
from .adapters import (
    SourceAdapterRegistry,
    EAIESourceAdapter,
    ELAESourceAdapter,
    ETAESourceAdapter,
    EQAESourceAdapter,
    EKDESourceAdapter,
    EDSESourceAdapter,
)


class EMIXEngine:
    """
    Point d'entrée principal du moteur EMIX.

    EMIX organise l'intégration de résultats issus
    de plusieurs moteurs analytiques EMIDAF.

    Il ne recalcule pas les analyses sources et ne
    produit pas automatiquement de conclusions
    scientifiques ou causales.
    """

    def create_adapter_registry(
        self,
    ) -> SourceAdapterRegistry:

        registry = SourceAdapterRegistry()

        registry.register(
            EAIESourceAdapter()
        )
        registry.register(
            ELAESourceAdapter()
        )
        registry.register(
            ETAESourceAdapter()
        )
        registry.register(
            EQAESourceAdapter()
        )
        registry.register(
            EKDESourceAdapter()
        )
        registry.register(
            EDSESourceAdapter()
        )

        return registry

    def adapt_source(
        self,
        *,
        engine: str,
        payload: dict,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        registry = (
            self.create_adapter_registry()
        )

        return registry.adapt(
            engine,
            payload,
            source_id=source_id,
            label=label,
        )

    def create_session(
        self,
    ) -> EMIXSession:

        registry = self.create_source_registry()

        integration = (
            self.create_integration_manager(
                registry
            )
        )

        joint_display = (
            self.create_joint_display_manager(
                integration
            )
        )

        inference = (
            self.create_meta_inference_manager(
                integration
            )
        )

        return EMIXSession(
            source_registry=registry,
            integration_manager=integration,
            joint_display_manager=joint_display,
            meta_inference_manager=inference,
        )

    def restore_session(
        self,
        payload: dict,
    ) -> EMIXSession:

        session = self.create_session()

        for item in payload.get(
            "sources",
            [],
        ):
            source = self.create_source(
                source_id=item["source_id"],
                engine=item["engine"],
                family=item["family"],
                label=item["label"],
                result_type=item["result_type"],
                result_ref=item.get(
                    "result_ref"
                ),
                description=item.get(
                    "description",
                    "",
                ),
            )

            session.source_registry.add(
                source
            )

        for item in payload.get(
            "links",
            [],
        ):
            link = self.create_link(
                link_id=item["link_id"],
                source_id_1=item["source_id_1"],
                source_id_2=item["source_id_2"],
                element_1=item["element_1"],
                element_2=item["element_2"],
                relation_type=item[
                    "relation_type"
                ],
                researcher_note=item.get(
                    "researcher_note",
                    "",
                ),
                candidate_id=item.get(
                    "candidate_id"
                ),
                validated=item.get(
                    "validated",
                    False,
                ),
            )

            session.integration_manager.add(
                link
            )

        for item in payload.get(
            "joint_display",
            [],
        ):
            row = (
                self.create_joint_display_row(
                    row_id=item["row_id"],
                    quantitative_result=item[
                        "quantitative_result"
                    ],
                    qualitative_result=item[
                        "qualitative_result"
                    ],
                    relation_type=item[
                        "relation_type"
                    ],
                    integrated_comment=item.get(
                        "integrated_comment",
                        "",
                    ),
                    source_link_id=item.get(
                        "source_link_id"
                    ),
                )
            )

            session.joint_display_manager.add(
                row
            )

        for item in payload.get(
            "meta_inferences",
            [],
        ):
            inference = (
                self.create_meta_inference(
                    inference_id=item[
                        "inference_id"
                    ],
                    statement=item[
                        "statement"
                    ],
                    link_ids=tuple(
                        item.get(
                            "link_ids",
                            [],
                        )
                    ),
                    limitations=tuple(
                        item.get(
                            "limitations",
                            [],
                        )
                    ),
                    researcher_note=item.get(
                        "researcher_note",
                        "",
                    ),
                    validated=item.get(
                        "validated",
                        False,
                    ),
                )
            )

            session.meta_inference_manager.add(
                inference
            )

        return session

    def create_source_registry(
        self,
    ) -> SourceRegistry:

        return SourceRegistry()

    def create_candidate_generator(
        self,
    ) -> IntegrationCandidateGenerator:

        return IntegrationCandidateGenerator()

    def create_candidate_converter(
        self,
        candidate_manager: IntegrationCandidateManager,
    ) -> CandidateToLinkConverter:

        return CandidateToLinkConverter(
            candidate_manager
        )

    def create_candidate_manager(
        self,
    ) -> IntegrationCandidateManager:

        return IntegrationCandidateManager()

    def create_candidate(
        self,
        *,
        source_1: MixedMethodSource,
        source_2: MixedMethodSource,
        element_1: str,
        element_2: str,
        rationale: str = "",
        candidate_id: str | None = None,
    ) -> IntegrationCandidate:

        generator = (
            self.create_candidate_generator()
        )

        return generator.generate(
            source_1=source_1,
            source_2=source_2,
            element_1=element_1,
            element_2=element_2,
            rationale=rationale,
            candidate_id=candidate_id,
        )

    def create_integration_manager(
        self,
        source_registry: SourceRegistry,
    ) -> IntegrationManager:

        return IntegrationManager(
            source_registry
        )

    def create_joint_display_manager(
        self,
        integration_manager: IntegrationManager,
    ) -> JointDisplayManager:

        return JointDisplayManager(
            integration_manager
        )

    def create_meta_inference_manager(
        self,
        integration_manager: IntegrationManager,
    ) -> MetaInferenceManager:

        return MetaInferenceManager(
            integration_manager
        )

    def create_source(
        self,
        *,
        source_id: str,
        engine: str,
        family: str,
        label: str,
        result_type: str,
        result_ref: str | None = None,
        description: str = "",
    ) -> MixedMethodSource:

        return MixedMethodSource(
            source_id=source_id,
            engine=engine,
            family=family,
            label=label,
            result_type=result_type,
            result_ref=result_ref,
            description=description,
        )

    def create_link(
        self,
        *,
        link_id: str,
        source_id_1: str,
        source_id_2: str,
        element_1: str,
        element_2: str,
        relation_type: str,
        researcher_note: str = "",
        candidate_id: str | None = None,
        validated: bool = False,
    ) -> IntegrationLink:

        return IntegrationLink(
            link_id=link_id,
            source_id_1=source_id_1,
            source_id_2=source_id_2,
            element_1=element_1,
            element_2=element_2,
            relation_type=relation_type,
            researcher_note=researcher_note,
            candidate_id=candidate_id,
            validated=validated,
        )

    def create_joint_display_row(
        self,
        *,
        row_id: str,
        quantitative_result: str,
        qualitative_result: str,
        relation_type: str,
        integrated_comment: str = "",
        source_link_id: str | None = None,
    ) -> JointDisplayRow:

        return JointDisplayRow(
            row_id=row_id,
            quantitative_result=quantitative_result,
            qualitative_result=qualitative_result,
            relation_type=relation_type,
            integrated_comment=integrated_comment,
            source_link_id=source_link_id,
        )

    def create_meta_inference(
        self,
        *,
        inference_id: str,
        statement: str,
        link_ids: tuple[str, ...] = (),
        limitations: tuple[str, ...] = (),
        researcher_note: str = "",
        validated: bool = False,
    ) -> MetaInference:

        return MetaInference(
            inference_id=inference_id,
            statement=statement,
            link_ids=link_ids,
            limitations=limitations,
            researcher_note=researcher_note,
            validated=validated,
        )

    def summarize_session(
        self,
        session: EMIXSession,
        *,
        candidates: list[
            IntegrationCandidate
        ] | None = None,
    ) -> MixedMethodsSummary:

        return self.create_summary(
            sources=(
                session.source_registry.all()
            ),
            candidates=(
                candidates or []
            ),
            links=(
                session.integration_manager.all()
            ),
            joint_display=(
                session.joint_display_manager.all()
            ),
            meta_inferences=(
                session.meta_inference_manager.all()
            ),
        )

    def create_summary(
        self,
        *,
        sources: list[MixedMethodSource],
        candidates: list[IntegrationCandidate] | None = None,
        links: list[IntegrationLink],
        joint_display: list[JointDisplayRow],
        meta_inferences: list[MetaInference],
    ) -> MixedMethodsSummary:

        return MixedMethodsSummary(
            sources=tuple(
                sources
            ),
            candidates=tuple(
                candidates or []
            ),
            links=tuple(
                links
            ),
            joint_display=tuple(
                joint_display
            ),
            meta_inferences=tuple(
                meta_inferences
            ),
        )
