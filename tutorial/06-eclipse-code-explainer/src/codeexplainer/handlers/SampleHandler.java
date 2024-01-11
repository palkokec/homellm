package codeexplainer.handlers;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.runtime.FileLocator;
import org.eclipse.core.runtime.Path;
import org.eclipse.core.runtime.Platform;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.ui.IWorkbenchPart;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.handlers.HandlerUtil;

public class SampleHandler extends AbstractHandler {

	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {

		try {
			//get active page file path
			IWorkbenchPart workbenchPart = PlatformUI.getWorkbench().getActiveWorkbenchWindow().getActivePage().getActivePart(); 
			File fileToAnalyze = (File) workbenchPart.getSite().getPage().getActiveEditor().getEditorInput().getAdapter(File.class);

			URL url = FileLocator.find(Platform.getBundle("code-explainer"), new Path("run.sh"), null);

			URL scriptUrl = FileLocator.toFileURL(url);

			ProcessBuilder processBuilder = new ProcessBuilder(scriptUrl.getPath(),fileToAnalyze.getAbsolutePath());
			Process process = processBuilder.start();

			// Optionally, wait for the process to complete
			process.waitFor();
			BufferedReader output = getOutput(process);
			BufferedReader error = getError(process);
			StringBuilder ob = new StringBuilder();
			String line = null;
			ob.append("Output:");
			ob.append(System.getProperty("line.separator"));
			while ((line = output.readLine()) != null) {
				ob.append(line);
				ob.append(System.getProperty("line.separator"));
			}
			ob.append("Error:");
			ob.append(System.getProperty("line.separator"));
			while ((line = error.readLine()) != null) {
				ob.append(line);
				ob.append(System.getProperty("line.separator"));
			}
			IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
			MessageDialog.openInformation(window.getShell(), "Code-explainer", ob.toString());

		} catch (IOException | InterruptedException e) {
			e.printStackTrace();
		}

		return null;
	}

	private static BufferedReader getOutput(Process p) {
		return new BufferedReader(new InputStreamReader(p.getInputStream()));
	}

	private static BufferedReader getError(Process p) {
		return new BufferedReader(new InputStreamReader(p.getErrorStream()));
	}
}
