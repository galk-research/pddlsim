Remote Simulator Protocol v1.0.0 (latest)
=========================================

While for some applications, no separation between the simulator and the agent is acceptable, for others, a client-server model is essential. In this model, there is absolute separation between the agent and the simulator, so that the agent cannot access any hidden information from the simulator, and a simulator may be used remotely, using the internet. For this, a "remote simulator" is used. Below, is the specification for the communication protocol between the client (henceforth, agent) and the server (henceforth, simulator).

Session phases and messages
---------------------------

The "Remote Simulator Protocol" (henceforth, "RSP") facilitates communication over a TCP connection between an agent and a simulator, for running a simulation session. Messages are written in `CBOR <https://cbor.io/>`__ and are unframed, as CBOR is self-delimiting. Throughout the specification, messages will be presented using `CDDL <https://datatracker.ietf.org/doc/rfc8610/>`__.

All messages sent will be of the form:

.. code-block:: cddl

    message = {
        type: text,
        payload: any,
    }

When message types will be introduced in the following sections, their ``type`` and their ``payload`` will both be detailed. Almost all messages are either a request, or a response. An agent may only send requests, and a simulator, only responses. Message types are unique among the corresponding kind of message, such that a response and a request may have the same type, but a different schema. The exception to this, are termination messages, which may be sent at any time, so either party must always be available to handle them.

Termination messages
~~~~~~~~~~~~~~~~~~~~

The following messages messages all terminate the session. They are noncontextual, and so may be sent no matter the context, no matter the time.

Give up
```````

A message of type ``give-up`` may be sent by the *agent* to indicate it has given up on solving the session problem. This message has a ``null`` payload.

Internal error
``````````````

A message of type ``error`` must be sent to indicate the session may not continue due to some error, which may originate from the sender, or from invalid data sent by receiver. The sesssion then must be terminated. This message has the following payload:

.. code-block:: cddl

    error = {
        kind: "internal" / "external",
        ? reason: text,
    }

Simulation termination
``````````````````````

A message of type ``simulation-termination`` may be sent by the *simulator* to indicate it is forcibly terminating the simulation. This may be done for any reason, and especially once the goal of a problem is reached (see `Peforming grounded actions`_). This message has the following payload:

.. code-block:: cddl

    simulation-termination = {
        ? reason: text,
    }

.. _Session setup:

Session setup
~~~~~~~~~~~~~

..
    * Should we add explicit support for asking for a specific problem?
    * Should we add support for agent authentication?

Once the communication channel is set up, the agent must send a ``session-setup`` request, with the following payload:

.. code-block:: cddl

    version = { major = uint, minor = uint }

    session-setup = {
        supported-versions: [* version],
    }

Once received, the simulator should send a ``session-setup`` response, with the following payload:

.. code-block:: cddl

    version = { major = uint, minor = uint }

    session-setup = {
        domain: text,
        problem: text,
        selected-version: version
    }

where ``domain`` and ``problem`` are both in the PPDDL-like language PDDLSIM uses, but without any revealable information (``:reveal``). ``selected-version`` will be the version selected by the simulator, out of ``supported-versions``.

Session operation
~~~~~~~~~~~~~~~~~

After `Session setup`_, the simulation has officialy begun. Session operation is the final stage of an RSP session, and where the bulk of its time is spent. In this phase, an agent may use a set of provided "services", and advance the simulation by performing grounded actions. All of this, using RSP requests.

Services
````````

"Services" is a collective name for requests that do not change the simulators external state. They may provide information on current and previous environment states, provide utilities for agent operation, and more.

Perception
''''''''''

The ``perception`` request allows an agent to get from the simulator the information it perceives in the current state, which is some fraction of the full simulated state, as some information may be hidden. It has a ``null`` payload. The ``perception`` response from the simulator must have this payload:

.. code-block:: cddl

    predicate-name = text
    object = text
    predicate-grounding = [* object]


    perception = {
        * predicate-name => [* predicate-grounding]
    }

Essentially, the returned information is information on all tuples of objects which satisfy a given predicate, for all predicates. For example, given state ``(west a b), (east b a)``, assuming all information should be known to the agent, the resulting payload would be ``{"west" => [["a", "b"]], "east" => [["b", "a"]]}``.

Get grounded actions
''''''''''''''''''''

The ``get-grounded-actions`` request allows the agent to receive the valid grounded actions it can perform in state, assuming the agent should be aware of them. Grounded actions relying on hidden information will not be shown. This request has a ``null`` payload. The response from the simulator is of the same type, and the following payload:

.. code-block:: cddl

    grounded-action = {
        name: text,
        grounding: [* object],
    }

    get-grounded-actions = [* grounded-action]


Goal tracking
'''''''''''''

The ``goals`` request allows the agent to receive information on which goals of the problem it has reached, and which, it has yet to reach. This request has a ``null`` payload. The response from the simulator has the same type, and the following payload:

.. code-block:: cddl

    goal = text

    goals = {
        reached: [* goal]
        unreached: [* goal],
    }

.. _Peforming grounded actions:

Performing grounded actions
```````````````````````````

For the agent to perform a grounded action, it must send a ``perform-grounded-action`` request, with the following payload:

.. code-block:: cddl

    object = text
    grounded-action = {
        name: text,
        grounding: [* object],
    }

    perform-grounded-action = grounded-action

Then, if the grounded action did not solve the problem after applying the grounded action, if the grounded action is valid, the response from the simulator is of the same type, and with the following payload:

.. code-block:: cddl

    effect-index = uint
    perform-grounded-action = effect-index

where ``effect-index`` is the index of the resulting effect of the action. This is only relevant for probabilistic actions, or fallible ones. If the grounded action received was invalid, it is assumed that the agent is erring, and so an external ``error`` response should be returned by the simulator.

If the grounded action instead *did* solve the problem, a ``simulation-termination`` response will be passed. the ``reason`` field is not constrained by this specification.

A simple example
----------------------

Consider an example problem, with the following PDDL domain:

.. code-block:: pddl

    (define (domain simple-domain)
            (:predicates (at ?location) (reachable ?a ?b))
            (:action move
             :parameters (?from ?to)
             :precondition (and (at ?from) (or (reachable ?to ?from) (reachable ?from ?to)))
             :effect (and (not (at ?from))
                          (at ?to))))

And a PDDL instance for it:

.. code-block:: pddl

    (define (problem simple-instance)
            (:domain simple-domain)
            (:objects ?a ?b ?c)
            (:init (at ?a)
                   (reachable ?a ?b)
                   (reachable ?b ?c))
            (:goal (at ?c)))

Given a simulator loaded with this problem, let's play the role of an agent, interacting with the simulator using the RSP protocol.

We will first requests a session setup, with the following request:

.. code-block:: cddl
    :caption: Sent by the agent

    {
        type: "session-setup",
        payload: null
    }

The simulator will then respond with a message accordingly, returning the PDDL strings used to simulate the problem. There isn't any hidden information, so the full strings seen above will be returned, like so:

.. code-block:: cddl
    :caption: Sent by the simulator

    {
        type: "session-setup",
        payload: {
            domain: "
                (define (domain simple-domain)
                        (:predicates (at ?location) (reachable ?a ?b))
                        (:action move
                        :parameters (?from ?to)
                        :precondition (and (at ?from) (or (reachable ?to ?from) (reachable ?from ?to)))
                        :effect (and (not (at ?from))
                                    (at ?to))))
            ",
            problem: "
                (define (problem simple-instance)
                        (:domain simple-domain)
                        (:objects a b c)
                        (:init (at a)
                            (reachable a b)
                            (reachable b c))
                        (:goal (at ?c)))
            ",
        }
    }

We can now begin to interact with the environment. To better understand our options though, let's first see which grounded actions we may perform, using the ``get-grounded-actions`` message type, sending a message like so:

.. code-block:: cddl
    :caption: Sent by the agent

    {
        type: "get-grounded-actions",
        payload: null
    }

The simulator will then respond as expected:

.. code-block:: cddl
    :caption: Sent by the simulator

    {
        type: "get-grounded-actions",
        payload: [
            {
                name: "move",
                grounding: ["a", "b"]
            },
        ],
    }

Note that one cannot do ``(move a a)``, as according to the problem, ``a`` is not reachable from ``a``. If ``(move a a)`` was possible, the problem could end up in a broken state, with our agent technically being "nowhere", due to how we implemented ``move``. Luckily, this isn't the case. Since we only have one valid grounded action, let's perform it, like so:

.. code-block:: cddl
    :caption: Sent by the agent

    {
        type: "perform-grounded-action",
        payload: {
            name: "move",
            grounding: ["a", "b"]
        },
    }

Being a valid grounded action, the simulator will respond with an effect index, as the domain is yet to be solved. This action is deterministic, and thus has a single effect, with effect index 0. Unsuprisingly, the simulator will respond with:

.. code-block:: cddl
    :caption: Sent by the simulator

    {
        type: "perform-grounded-action",
        payload: 0,
    }

Great! We're one step closer to solving the problem. Let's see what our surroundings look like now, using the perception service:

.. code-block:: cddl
    :caption: Sent by the agent

    {
        type: "perception",
        payload: null,
    }

This is the environment state returned by the simulator:


.. code-block:: cddl
    :caption: Sent by the simulator

    {
        type: "perception",
        payload: {
            "at" => [["b"]],
            "reachable" => [["a", "b"], ["b", "c"]],
            "=" => [["a", "a"], ["b", "b"], ["c", "c"]]
        },
    }

Wait, what? What's this ``"="`` predicate doing here? While it doesn't appear anywhere in the domain definition, PDDLSIM automatically added it to the problem state, as one can use equality constraints in preconditions. Beyond this idiosyncraticity, the current state is fairly understandable. Let's now finish the problem, by moving to ``c``:

.. code-block:: cddl
    :caption: Sent by the agent

    {
        type: "perform-grounded-action",
        payload: {
            name: "move",
            grounding: ["b", "c"],
        },
    }

As we have now finished the problem, we simulator will respond with the closing of the session, like so:

.. code-block:: cddl
    :caption: Sent by the simulator

    {
        type: "session-termination",
        payload: {
            reason: "problem solved",
        },
    }

We should now disconnect from the server's port.