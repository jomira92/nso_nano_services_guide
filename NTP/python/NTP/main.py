"""NSO Nano service example.

Implements a Nano service callback
(C) 2023 Cisco Systems
Permission to use this code as a starting point hereby granted

See the README file for more information
"""
import ncs
from ncs.application import NanoService


# -----------------------------
# NANO SERVICE CALLBACK EXAMPLE
# -----------------------------
class NanoServiceCallbacks(NanoService):
    '''Nano service callbacks'''
    @NanoService.create
    def cb_nano_create(self, tctx, root, service, plan, component, state,
                       proplist, component_proplist):
        '''Nano service create callback'''
        self.log.info('Nano create(state=', state, ')')

        if state == 'NTP:server-configured':
            vars = ncs.template.Variables()
            vars.add('DUMMY', '127.0.0.1')
            template = ncs.template.Template(service)
            template.apply('NTP-template-1-server', vars)

        elif state == 'NTP:peer-configured':
            vars = ncs.template.Variables()
            vars.add('DUMMY', '127.0.0.1')
            template = ncs.template.Template(service)
            template.apply('NTP-template-2-peer', vars)

        elif state == 'NTP:max-associations-configured':
            vars = ncs.template.Variables()
            vars.add('DUMMY', '127.0.0.1')
            template = ncs.template.Template(service)
            template.apply('NTP-template-3-max', vars)

    # @NanoService.delete
    # def cb_nano_delete(self, tctx, root, service, plan, component, state,
    #                    proplist, component_proplist):


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    '''Nano service appliction implementing the nano create callback'''
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Nano service callbacks require a registration for a service point,
        # component, and state, as specified in the corresponding data model
        # and plan outline.
        self.register_nano_service('NTP-servicepoint',  # Service point
                                   'ncs:self',              # Component
                                   'NTP:server-configured',       # State
                                   NanoServiceCallbacks)
        
        self.register_nano_service('NTP-servicepoint',  # Service point
                                    'ncs:self',              # Component
                                    'NTP:peer-configured',       # State
                                    NanoServiceCallbacks)

        self.register_nano_service('NTP-servicepoint',  # Service point
                                    'ncs:self',              # Component
                                    'NTP:max-associations-configured',       # State
                                    NanoServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')