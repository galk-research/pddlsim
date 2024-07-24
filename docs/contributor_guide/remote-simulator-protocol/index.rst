.. _Remote Simulator Protocol:

Remote Simulator Protocol
=========================

While for some applications, no separation between the simulator and the agent is acceptable, for others, a client-server model is essential. In this model, there is absolute separation between the agent and the simulator, so that the agent cannot access any hidden information from the simulator, and a simulator may be used remotely, using the internet. For this, a "remote simulator" is used. Below, is the specification for the communication protocol between the client (henceforth, agent) and the server (henceforth, simulator).

.. _Versioning guarantees:

Versioning guarantees
---------------------

RSP protocol versions are of the form ``vX.Y``, where ``X`` is the major release number, and ``Y`` is the minor release number, starting from ``v1.0``. The minor release number will be incremented when new "common types" are added, but nothing else is changed in the specification. A version ``vA.B`` is agent-compatible with another version ``vC.D``, if ``A == C`` and ``B >= D``. In other words, an agent-compatible version, is one where the agent will never be able observe a difference in version. A simulator-compatible version is the same, but with the comparison flipped, ``B <= D``. When deciding on a version for a protocol session, the agent will present a series of versions, such that any other version agent-compatible with them, will be acceptable for communication. Such a version exists, assuming it is also simulator-compatible with some version supported by the simulator, given a final compatibility requirement for a version ``vA.B``, over agent-supported version ``vC.D``, and simulator-supported version ``vE.F``, of ``A == B == C``, ``D <= B <= F``.

..
    Should we really do nothing here? Maybe add support for "patch" versions? Its unclear if just ditching the buggy versions is the right call. What if migration to a new version is too hard? Then again, this probably won't happen in practice, as the protocol will only be used by PDDLSIM internally

Should a phrasing error, typo, logic error, or any kind of error be spotted in a version, current or previous, if the error will be deemed nonconsequential on communication, such as in cases where the error is related to an edge-case not encountered in practical communication, or assuming most people's interpretation of the errant section, was the intended one, that version's specification may be updated to reflect this. Otherwise, if the version is current, a new one should be released. Otherwise, nothing will be done, as the version should already be considered legacy.

Specifications
--------------

Below are the different specifications of each RSP protocol version, in reverse-chronological order. The latest version is marked "latest".

.. toctree::
    :maxdepth: 1

    latest