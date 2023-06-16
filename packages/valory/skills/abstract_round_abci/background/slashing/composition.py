# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022-2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the slashing background app composition."""

from packages.valory.skills.abstract_round_abci.abci_app_chain import (
    AbciAppTransitionMapping,
    chain,
)
from packages.valory.skills.abstract_round_abci.background.slashing.round import (
    PostSlashingTxAbciApp,
    SlashingCheckRound,
    Event,
)
from packages.valory.skills.transaction_settlement_abci.rounds import (
    FinishedTransactionSubmissionRound,
    TransactionSubmissionAbciApp,
    FailedRound,
)


slashing_transition_function: AbciAppTransitionMapping = {
    FinishedTransactionSubmissionRound: PostSlashingTxAbciApp.initial_round_cls,
    FailedRound: TransactionSubmissionAbciApp.initial_round_cls,
}
SlashingAbciApp = chain(
    (
        TransactionSubmissionAbciApp,
        PostSlashingTxAbciApp,
    ),
    slashing_transition_function,
)

SlashingAbciApp.transition_function[SlashingCheckRound] = {
    Event.SLASH_START: TransactionSubmissionAbciApp.initial_round_cls,
}
